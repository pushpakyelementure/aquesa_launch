from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone
from pydantic import UUID4
import calendar

from app.db.models.aqs_enums import aggregation_enum
from app.db.models.consumption import rawdata


async def daily_data(
    user_token: str,
    communityid: UUID4,
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

    try:
        community = await rawdata.find_one(rawdata.communityid == communityid)

        if community is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Community Not found",
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

    try:

        # Define the aggregation pipeline
        pipeline = [
            {
                "$match": {
                    "devicetime": {
                        "$gte": start_dt,
                        "$lt": end_dt,
                    },
                    "communityid": communityid,  # Noqa
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

        # Initialize all days with 0 consumption
        current_date = start_dt.date()
        end_date = end_dt.date()
        all_days_consumption = {}
        while current_date <= end_date:
            all_days_consumption[
                (current_date.year, current_date.month, current_date.day)
            ] = 0
            current_date += timedelta(days=1)

        # Update with actual data from results
        for item in result:
            date_key = (
                item["_id"]["year"],
                item["_id"]["month"],
                item["_id"]["day"],
            )
            all_days_consumption[date_key] = round(item["daily_consumption"])

        # Prepare response data
        # response_data = []
        total_consumption = 0
        for date, consumption in all_days_consumption.items():
            year, month, day = date
            total_consumption += consumption
            # formatted_data = {
            #     "year": str(year),
            #     "month": str(month).zfill(2),
            #     "date": str(day).zfill(2),
            #     "aggregation": aggregation_enum.day,
            #     "consumption": [consumption],
            # }
            # response_data.append(formatted_data)

        response = {
            "total_consumption": int(total_consumption),
            # "data": response_data,
        }

        return response

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


async def weekly_data(
    user_token: str,
    communityid: UUID4,
    start_ist: datetime,
):
    # Calculate start and end of the week (assuming Monday as the first day of the week) # noqa
    start_of_week = start_ist - timedelta(days=start_ist.weekday())
    end_of_week = start_of_week + timedelta(
        days=6, hours=23, minutes=59, seconds=59
    )  # noqa

    try:
        community = await rawdata.find_one(rawdata.communityid == communityid)

        if community is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Community Not found",
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

    try:
        # Define the aggregation pipeline
        pipeline = [
            {
                "$match": {
                    "devicetime": {
                        "$gte": start_of_week,
                        "$lt": end_of_week,
                    },
                    "communityid": communityid,
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

        # Initialize weekly consumption dictionary
        grouped_results = {
            (start_of_week + timedelta(days=i)).strftime("%Y-%m-%d"): 0
            for i in range(7)  # noqa
        }

        for item in result:
            day = datetime(
                item["_id"]["year"], item["_id"]["month"], item["_id"]["day"]
            ).strftime(
                "%Y-%m-%d"
            )  # noqa
            grouped_results[day] = round(item["daily_consumption"])

        # # Prepare response data
        # response_data = {
        #     "year": str(start_of_week.year),
        #     "month": str(start_ist.month).zfill(2),
        #     "date": None,
        #     "aggregation": aggregation_enum.week,
        #     "consumption": list(grouped_results.values()),
        # }

        total_consumption = sum(grouped_results.values())
        response = {
            "total_consumption": int(total_consumption),
            # "data": [response_data],
        }

        return response

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


async def monthly_data(
    user_token: str,
    communityid: UUID4,
    start_ist: datetime,
):
    # Convert the start and end date which is in datetime.date format to a
    # datetime.datetime object where
    # start time is 00:00:00 and end time is 23:59:59
    start_dt = datetime(
        start_ist.year,
        start_ist.month,
        1,
        0,
        0,
        0,
    )
    end_dt = datetime(
        start_ist.year,
        start_ist.month,
        calendar.monthrange(start_ist.year, start_ist.month)[1],
        23,
        59,
        59,
    )

    try:
        community = await rawdata.find_one(rawdata.communityid == communityid)

        if community is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Community Not found",
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

    try:

        # Define the aggregation pipeline
        pipeline = [
            {
                "$match": {
                    "devicetime": {
                        "$gte": start_dt,
                        "$lt": end_dt,
                    },
                    "communityid": communityid,  # Noqa
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

        # Group the results by date
        # Process the results
        grouped_results = {
            day: 0
            for day in range(
                1, calendar.monthrange(start_ist.year, start_ist.month)[1] + 1
            )
        }
        for item in result:
            day = item["_id"]["day"]
            grouped_results[day] = round(item["daily_consumption"])

        # # Prepare response data
        # response_data = {
        #     "year": str(start_ist.year),
        #     "month": str(start_ist.month).zfill(2),
        #     "date": None,
        #     "aggregation": aggregation_enum.month,
        #     "consumption": list(grouped_results.values()),
        # }

        total_consumption = sum(grouped_results.values())
        response = {
            "total_consumption": int(total_consumption),
            # "total_consumption_limit": limit * limit_for,  # Example value
            # "data": [response_data],
        }

        return response

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


# Month Top 5 Dwelling Consumptions
async def month_top_dwellings_consumption(
    user_token: str,
    communityid: UUID4,  # Input is 'communityid'
    start_ist: datetime,
    end_ist: datetime,
    aggregation: aggregation_enum,
    limit: int = 5,  # Default to top 5 dwellings
):
    start_dt = datetime(start_ist.year, start_ist.month, 1, 0, 0, 0)
    end_dt = datetime(
        start_ist.year,
        start_ist.month,
        calendar.monthrange(start_ist.year, start_ist.month)[-1],
        23,
        59,
        59,  # noqa
    )

    try:
        community = await rawdata.find_one({"communityid": communityid})
        if community is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Community Not found",
            )

        # Determine the grouping key based on the aggregation type
        if aggregation == aggregation_enum.month:
            # group_by = {"$month": "$devicetime"}
            group_by = {
                "$dateToString": {
                    "format": "%B",  # Full month name (e.g., January)
                    "date": "$devicetime",
                }
            }
        elif aggregation == aggregation_enum.week:
            group_by = {"$isoWeek": "$devicetime"}
        elif aggregation == aggregation_enum.day:
            group_by = {"$dayOfMonth": "$devicetime"}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid aggregation type",
            )

        # Aggregation pipeline
        pipeline = [
            {
                "$match": {
                    "devicetime": {"$gte": start_dt, "$lt": end_dt},
                    "communityid": communityid,
                }
            },
            {
                "$group": {
                    "_id": {
                        "dwellingid": "$dwellingid",
                        "period": group_by,
                    },
                    "total_consumption": {"$sum": "$data.evt.csm"},
                }
            },
            {"$sort": {"total_consumption": -1}},
            {"$limit": limit},  # Get top dwellings
        ]

        # Execute aggregation
        result = await rawdata.aggregate(pipeline).to_list(length=None)

        # ✅ Corrected response field names
        response_data = {
            "aggregation": aggregation.value,
            "community_id": communityid,
            "top_5_dwellings": [
                {
                    "dwelling_id": item["_id"]["dwellingid"],
                    "total_consumption": round(item["total_consumption"]),
                }
                for item in result
            ],
        }
        return response_data

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


async def week_top_dwellings_consumption(
    user_token: str,
    communityid: UUID4,
    start_ist: datetime,
    end_ist: datetime,
    aggregation: aggregation_enum,
    limit: int = 5,
):
    start_dt = datetime(start_ist.year, start_ist.month, 1, 0, 0, 0)
    end_dt = datetime(
        start_ist.year,
        start_ist.month,
        calendar.monthrange(start_ist.year, start_ist.month)[1],
        23,
        59,
        59,  # noqa
    )

    try:
        community = await rawdata.find_one({"communityid": communityid})
        if community is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Community Not found",
            )

        # Determine the grouping key based on the aggregation type
        if aggregation == aggregation_enum.month:
            group_by = {
                "$dateToString": {
                    "format": "%B",  # Full month name (e.g., January)
                    "date": "$devicetime",
                }
            }
        elif aggregation == aggregation_enum.week:
            group_by = {"$isoWeek": "$devicetime"}  # Group by ISO week
        elif aggregation == aggregation_enum.day:
            group_by = {"$dayOfMonth": "$devicetime"}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid aggregation type",
            )

        # Aggregation pipeline
        pipeline = [
            {
                "$match": {
                    "devicetime": {"$gte": start_dt, "$lt": end_dt},
                    "communityid": communityid,
                }
            },
            {
                "$group": {
                    "_id": {
                        "dwellingid": "$dwellingid",
                        "period": group_by,  # This will group by week
                    },
                    "total_consumption": {"$sum": "$data.evt.csm"},
                }
            },
            {"$sort": {"total_consumption": -1}},
            {"$limit": limit},  # Get top dwellings
        ]

        # Execute aggregation
        result = await rawdata.aggregate(pipeline).to_list(length=None)

        # Response
        response_data = {
            "aggregation": aggregation.value,
            "community_id": str(communityid),
            "top_5_dwellings": [
                {
                    "dwelling_id": str(item["_id"]["dwellingid"]),
                    "total_consumption": round(item["total_consumption"]),
                    "period": item["_id"]["period"],
                }
                for item in result
            ],
        }
        return response_data

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


async def day_top_dwellings_consumption(
    user_token: str,
    communityid: UUID4,
    start_ist: datetime,
    end_ist: datetime,
    aggregation: aggregation_enum,
    limit: int = 5,
):
    start_dt = datetime(start_ist.year, start_ist.month, 1, 0, 0, 0)
    end_dt = datetime(
        start_ist.year,
        start_ist.month,
        calendar.monthrange(start_ist.year, start_ist.month)[1],
        23,
        59,
        59,  # noqa
    )

    try:
        community = await rawdata.find_one({"communityid": communityid})
        if community is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Community Not found",
            )

        # Determine the grouping key based on the aggregation type
        if aggregation == aggregation_enum.month:
            group_by = {
                "$dateToString": {
                    "format": "%B",  # Full month name (e.g., January)
                    "date": "$devicetime",
                }
            }
        elif aggregation == aggregation_enum.week:
            group_by = {"$isoWeek": "$devicetime"}  # Group by ISO week
        elif aggregation == aggregation_enum.day:
            group_by = {"$dayOfMonth": "$devicetime"}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid aggregation type",
            )

        # Aggregation pipeline
        pipeline = [
            {
                "$match": {
                    "devicetime": {"$gte": start_dt, "$lt": end_dt},
                    "communityid": communityid,
                }
            },
            {
                "$group": {
                    "_id": {
                        "dwellingid": "$dwellingid",
                        "period": group_by,  # This will group by week
                    },
                    "total_consumption": {"$sum": "$data.evt.csm"},
                }
            },
            {"$sort": {"total_consumption": -1}},
            {"$limit": limit},  # Get top dwellings
        ]

        # Execute aggregation
        result = await rawdata.aggregate(pipeline).to_list(length=None)

        # Response
        response_data = {
            "aggregation": aggregation.value,
            "community_id": str(communityid),
            "top_5_dwellings": [
                {
                    "dwelling_id": str(item["_id"]["dwellingid"]),
                    "total_consumption": round(item["total_consumption"]),
                    "period": item["_id"]["period"],
                }
                for item in result
            ],
        }
        return response_data

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


# async def dwelling_monthly_consumption(
#     user_token: str,
#     communityid: UUID4,
#     dwellingid: UUID4,
#     start_ist: datetime,
#     end_ist: datetime,
#     aggregation: aggregation_enum,
# ):
#     # Convert IST to UTC before querying MongoDB
#     start_dt = datetime(
#         start_ist.year, start_ist.month, 1, 0, 0, 0, tzinfo=timezone.utc
#     )  # noqa
#     end_dt = datetime(
#         end_ist.year, end_ist.month, 1, 0, 0, 0, tzinfo=timezone.utc
#     )  # noqa
#     try:
#         # Check if community exists
#         community = await rawdata.find_one({"communityid": communityid})
#         if community is None:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail="Community Not found",
#             )
#         dwelling = await rawdata.find_one({"dwellingid": dwellingid})
#         if dwelling is None:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail="Community Not found",
#             )

#         # Aggregation pipeline
#         pipeline = [
#             {
#                 "$match": {
#                     "devicetime": {"$gte": start_dt, "$lt": end_dt},
#                     "communityid": communityid,
#                     "dwellingid": dwellingid,
#                 }
#             },
#             {
#                 "$group": {
#                     "_id": {"month": {"$month": "$devicetime"}},
#                     "total_consumption": {"$sum": "$data.evt.csm"},
#                 }
#             },
#         ]

#         # Execute aggregation
#         result = await rawdata.aggregate(pipeline).to_list(length=None)

#         # Extract total consumption
#         total_consumption = result[0]["total_consumption"] if result else 0

#         # Construct response
#         response_data = {
#             "year": start_ist.year,
#             "month": start_ist.month,
#             "date": None,
#             "aggregation": aggregation_enum.month,
#             "consumption": [
#                 total_consumption
#             ],  # Store total monthly consumption in a list
#         }

#         response = {
#             "total_consumption": int(total_consumption),
#             "community_id": communityid,
#             "dwelling_id": dwellingid,
#             "consumption_data": response_data,  # Use corrected data model
#         }

#         return response

#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=str(e),
#         )


# async def dwelling_day_consumption(
#     user_token: str,
#     communityid: UUID4,
#     dwellingid: UUID4,
#     start_ist: datetime,
#     end_ist: datetime,
#     aggregation: aggregation_enum,
# ):

#     start_dt = datetime(
#         start_ist.year,
#         start_ist.month,
#         start_ist.day,
#         0,
#         0,
#         0,
#     )
#     end_dt = datetime(
#         end_ist.year,
#         end_ist.month,
#         end_ist.day,
#         23,
#         59,
#         59,
#     )

#     try:
#         # Check if community exists
#         community = await rawdata.find_one({"communityid": communityid})
#         if community is None:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail="Community Not found",
#             )
#         dwelling = await rawdata.find_one({"dwellingid": dwellingid})
#         if dwelling is None:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail="Dwelling Not found",
#             )

#         # Aggregation pipeline
#         pipeline = [
#             {
#                 "$match": {
#                     "devicetime": {
#                         "$gte": start_dt,
#                         "$lt": end_dt,
#                     },
#                     "communityid": communityid,
#                     "dwelling": dwellingid,  # Noqa
#                 }
#             },
#             {
#                 "$group": {
#                     "_id": {
#                         "year": {"$year": "$devicetime"},
#                         "month": {"$month": "$devicetime"},
#                         "day": {"$dayOfMonth": "$devicetime"},
#                     },
#                     "daily_consumption": {"$sum": "$data.evt.csm"},
#                 }
#             },
#             {
#                 "$project": {
#                     "_id": 1,
#                     "daily_consumption": 1,
#                     "year": "$_id.year",
#                     "month": "$_id.month",
#                     "day": "$_id.day",
#                 }
#             },
#             {"$sort": {"_id": 1}},
#         ]

#         # Execute aggregation
#         result = await rawdata.aggregate(pipeline).to_list(length=None)

#         # Initialize all days with 0 consumption
#         current_date = start_dt.date()
#         end_date = end_dt.date()
#         all_days_consumption = {}
#         total_consumption = 0  # Initialize total consumption

#         while current_date <= end_date:
#             all_days_consumption[
#                 (current_date.year, current_date.month, current_date.day)
#             ] = 0
#             current_date += timedelta(days=1)

#         # Update with actual data from results
#         for item in result:
#             date_key = (
#                 item["year"],
#                 item["month"],
#                 item["day"],
#             )
#             all_days_consumption[date_key] = round(item["daily_consumption"])
#             total_consumption += round(item["daily_consumption"])

#         # Prepare response data
#         response_data = []
#         for date, consumption in all_days_consumption.items():
#             year, month, day = date
#             formatted_data = {
#                 "year": str(year),
#                 "month": str(month).zfill(2),
#                 "date": str(day).zfill(2),
#                 "aggregation": aggregation.value,  # Convert Enum to string
#                 "consumption": consumption,  # Ensure it's a number, not a list
#             }
#             response_data.append(formatted_data)

#         # Use ConsumptionResponse model for the final response
#         response = {
#             "total_consumption": int(total_consumption),
#             "community_id": str(communityid),  # Convert UUID to string
#             "dwelling_id": str(dwellingid),  # Convert UUID to string
#             "consumption_data": response_data,
#         }

#         return response

#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=str(e),
#         )
