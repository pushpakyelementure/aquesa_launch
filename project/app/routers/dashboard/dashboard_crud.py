from fastapi import HTTPException, status
from pydantic import UUID4
from datetime import datetime, timedelta
import statistics
from app.db.models.dwelling import dwelling_model
from app.db.models.consumption import rawdata
from app.db.models.csm_limit import day_limit


# Read a community info
async def get_community_info_by_id(community_id):
    comm = await dwelling_model.find_one(
        dwelling_model.community_id == community_id
    )  # noqa
    if comm is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="community not found",
        )

    flats = await dwelling_model.find(
        dwelling_model.community_id == community_id,
    ).to_list() # noqa

    return flats
 

async def block_data(
    user_token: str,
    community_id: UUID4,
    start_ist: datetime,
    end_ist: datetime,
):
    # Convert the start and end date which is in datetime.date format to a
    # datetime.datetime object where
    # start time is 00:00:00 and end time is 23:59:59
    start_dt = datetime(
        start_ist.year,
        start_ist.month,
        start_ist.day,
        0,
        0,
        0,
    )
    end_dt = datetime(
        end_ist.year,
        end_ist.month,
        end_ist.day,
        23,
        59,
        59,
    )

    # Ensure the community exists in rawdata collection
    community = await rawdata.find_one({"communityid": community_id})
    if community is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Community Not found",
        )

    # Fetch dwellings with aggregation
    try:

        dwellings_pipeline = [
            {"$match": {"community_id": community_id}},
            {"$group": {"_id": "$block", "dwelling_ids": {"$push": "$dwelling_id"}}}
        ]
        dwellings_cursor = dwelling_model.aggregate(dwellings_pipeline)
        dwellings = await dwellings_cursor.to_list(length=None)

        if not dwellings:
            raise HTTPException(status_code=404, detail="Community Not Found")


        # Extract dwelling IDs as BSON Binary
        dwelling_ids = [dw_id for block in dwellings for dw_id in block["dwelling_ids"]]    # Fetch consumption data
        rawdata_pipeline = [
            {"$match": {
                "dwellingid": {"$in": dwelling_ids},
                "datatime": {"$gte": start_dt, "$lte": end_dt}
            }},
            {"$group": {
                "_id": "$dwellingid",
                "total_csm": {"$sum": {"$ifNull": ["$data.evt.csm", 0]}}
            }}
        ]
        rawdata_cursor = rawdata.aggregate(rawdata_pipeline)
        rawdata_results = await rawdata_cursor.to_list(length=None)

        # Map consumption per dwelling
        dwelling_csm_map = {entry["_id"]: entry["total_csm"] for entry in rawdata_results}

        # Compute block-level CSM totals
        block_csm_totals = {
            block["_id"]: sum(dwelling_csm_map.get(dwelling_id, 0) for dwelling_id in block["dwelling_ids"])
            for block in dwellings
        }

        return {"blockwise_consumption": block_csm_totals}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


async def water_usage_day(
    user_token: str,
    community_id: UUID4,
    start_ist: datetime,
    end_ist: datetime,
):
    # Convert the start and end date which is in datetime.date format to a
    # datetime.datetime object where
    # start time is 00:00:00 and end time is 23:59:59
    start_dt = datetime(
        start_ist.year,
        start_ist.month,
        start_ist.day,
        0,
        0,
        0,
    )
    end_dt = datetime(
        end_ist.year,
        end_ist.month,
        end_ist.day,
        23,
        59,
        59,
    )
    # Ensure the community exists in rawdata collection
    community = await rawdata.find_one({"communityid": community_id})
    if community is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Community Not found",
        )
    try:

        # Step 1: Get all unique dwellings for this community
        dwellings = await rawdata.distinct("dwellingid", {"communityid": community_id})
        
        if not dwellings:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No dwellings found for this community",
            )

    # Fetch limits from `day_limit`
        dwelling_limits = await day_limit.find({"dwelling_id": {"$in": dwellings}}).to_list(length=None)

        total_limit = sum(d.limit for d in dwelling_limits if hasattr(d, "limit"))    


    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

    # Step 3: Compute daily consumption
    pipeline = [
        {
            "$match": {
                "devicetime": {
                    "$gte": start_dt,
                    "$lt": end_dt,
                },
                "communityid": community_id,
            }
        },
        {
            "$group": {
                "_id": {
                    "year": {"$year": "$devicetime"},
                    "month": {"$month": "$devicetime"},
                    "day": {"$dayOfMonth": "$devicetime"},
                },
                "daily_consumption": {"$sum": "$data.evt.csm"},
            }
        },
        {"$sort": {"_id": 1}},
    ]

    # Execute the aggregation pipeline
    result = await rawdata.aggregate(pipeline).to_list(length=None)

    # Step 4: Initialize all days with 0 consumption
    current_date = start_dt.date()
    end_date = end_dt.date()
    all_days_consumption: Dict = {}

    while current_date <= end_date:
        all_days_consumption[(current_date.year, current_date.month, current_date.day)] = 0
        current_date += timedelta(days=1)

    # Update with actual data from results
    for item in result:
        date_key = (item["_id"]["year"], item["_id"]["month"], item["_id"]["day"])
        all_days_consumption[date_key] = round(item["daily_consumption"])

    # Step 5: Calculate total consumption
    total_consumption = sum(all_days_consumption.values())
    # average_consumption = total_consumption/24

    csm_values = [item["daily_consumption"] for item in result if "daily_consumption" in item and isinstance(item["daily_consumption"], (int, float))]

    # **Ensure we have valid values before calculating mean**
    if csm_values:
        average_csm = round(statistics.mean(csm_values), 2)
    else:
        average_csm = 0

    excess_csm = total_limit - total_consumption
    if excess_csm > total_limit:
        excess_com = round(excess_csm)
    else:
        excess_com = 0
        

    # Compute the single average of all CSM values
    average_csm = round(statistics.mean(csm_values), 2) if csm_values else 0
    # Step 6: Compare total consumption with the total limit
    response = {
        "total_consumption": int(total_consumption),
        "average_consumption": int(round(average_csm/24)),
        "total_limit": int(total_limit),
        "excess_consumption": excess_com,
        "status": "Exceeded Limit" if total_consumption > total_limit else "Within Limit",
    }

    return response


async def water_usage_week(
    user_token: str,
    community_id: UUID4,
    start_ist: datetime,
    # end_ist: datetime,
):
    # Convert start & end dates to datetime range (from 00:00:00 to 23:59:59)
    start_of_week = start_ist - timedelta(days=start_ist.weekday())
    end_of_week = start_of_week + timedelta(
        days=6, hours=23, minutes=59, seconds=59
    )  # noqa

    # Ensure the community exists in rawdata collection
    community = await rawdata.find_one({"communityid": community_id})
    if community is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Community Not found",
        )

    try:
        # Step 1: Get all unique dwellings for this community
        dwellings = await rawdata.distinct("dwellingid", {"communityid": community_id})

        if not dwellings:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No dwellings found for this community",
            )

        # Step 2: Fetch the total limit for all dwellings from `day_limit`
        dwelling_limits = await day_limit.find({"dwelling_id": {"$in": dwellings}}).to_list(length=None)
        dwelling_limit = [dict(d) for d in dwelling_limits]  # Convert to dictionary
        total_limit = sum(d["limit"] * 7 for d in dwelling_limit if "limit" in d)
        print(total_limit)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

    # Step 3: Compute weekly consumption
    pipeline = [
        {
            "$match": {
                "devicetime": {
                    "$gte": start_of_week,
                    "$lt": end_of_week,
                },
                "communityid": community_id,
            }
        },
        {
            "$group": {
                "_id": {
                    "year": {"$year": "$devicetime"},
                    "week": {"$isoWeek": "$devicetime"},  # Group by ISO week
                },
                "weekly_consumption": {"$sum": "$data.evt.csm"},
            }
        },
        {"$sort": {"_id": 1}},
    ]

    # Execute the aggregation pipeline
    result = await rawdata.aggregate(pipeline).to_list(length=None)

    # Step 4: Initialize all weeks with 0 consumption
    current_week = start_of_week.isocalendar()[1]  # Get starting week number
    end_week = end_of_week.isocalendar()[1]  # Get ending week number
    all_weeks_consumption: Dict = {}

    while current_week <= end_week:
        all_weeks_consumption[(start_of_week.year, current_week)] = 0
        current_week += 1

    # Update with actual data from results
    for item in result:
        week_key = (item["_id"]["year"], item["_id"]["week"])
        all_weeks_consumption[week_key] = round(item["weekly_consumption"])

    # Step 5: Calculate total consumption
    total_consumption = sum(all_weeks_consumption.values())
    average_consumption = total_consumption / 7 if total_consumption else 0

    excess_csm = total_limit - total_consumption
    if excess_csm > total_limit:
        excess_com = round(excess_csm)
    else:
        excess_com = 0

    # Step 6: Compare total consumption with the total limit
    response = {
        "total_consumption": int(total_consumption),
        "average_consumption": int(average_consumption),
        "total_limit": int(total_limit),
        "excess_consumption": excess_com,
        "status": "Exceeded Limit" if total_consumption > total_limit else "Within Limit",
    }

    return response


async def water_usage_month(
    user_token: str,
    community_id: UUID4,
    start_ist: datetime,
):
    # Convert start date to the first day of the month (00:00:00) & last day of the month (23:59:59)
    start_of_month = datetime(start_ist.year, start_ist.month, 1)
    next_month = start_of_month.replace(day=28) + timedelta(days=4)  # Move to the next month
    end_of_month = next_month - timedelta(days=next_month.day)  # Get the last day of this month
    pipeline = []

    # Ensure the community exists in rawdata collection
    community = await rawdata.find_one({"communityid": community_id})
    if community is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Community Not found",
        )

    try:

        # Step 1: Get all unique dwellings for this community
        dwellings = await rawdata.distinct("dwellingid", {"communityid": community_id})

        if not dwellings:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No dwellings found for this community",
            )

        # Step 2: Fetch the total limit for all dwellings from `day_limit`
        dwelling_limits = await day_limit.find({"dwelling_id": {"$in": dwellings}}).to_list(length=None)
        dwelling_limit = [dict(d) for d in dwelling_limits]  # Convert to dictionary
        
        # Calculate total monthly limit (limit per day × number of days in the month)
        days_in_month = (end_of_month - start_of_month).days + 1
        total_limit = sum(d["limit"] * days_in_month for d in dwelling_limit if "limit" in d)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
        
    pipeline = [
    {
        "$match": {
            "devicetime": {
                "$gte": start_of_month,
                "$lt": end_of_month,
            },
            "communityid": community_id,
        }
    },
    {
        "$group": {
            "_id": {
                "year": {"$year": "$devicetime"},
                "month": {"$month": "$devicetime"},
                "day": {"$dayOfMonth": "$devicetime"},  # Group by year, month, and day
            },
            "daily_consumption": {"$sum": "$data.evt.csm"},  # Sum csm per day
        }
        },
        {"$sort": {"_id": 1}},
    ]

    # Execute the aggregation pipeline
    result = await rawdata.aggregate(pipeline).to_list(length=None)


    daily_consumption_values = []

    for item in result:
        daily_consumption_values.append(item["daily_consumption"])

    # Compute total and average daily consumption
    total_consumption = sum(daily_consumption_values)
    days_count = len(daily_consumption_values)

    # Avoid division by zero
    average_daily_consumption = round(total_consumption / days_count, 2) if days_count > 0 else 0

    excess_csm = total_limit - total_consumption
    if excess_csm > total_limit:
        excess_com = round(excess_csm)
    else:
        excess_com = 0
        
    # Compare with the total limit
    response = {
        "total_consumption": int(total_consumption),
        "average_consumption": int(average_daily_consumption),
        "total_limit": int(total_limit),
        "excess_consumption": excess_com,
        "status": "Exceeded Limit" if total_consumption > total_limit else "Within Limit",
    }

    return response
