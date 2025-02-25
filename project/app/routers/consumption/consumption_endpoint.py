from fastapi import APIRouter, status, Depends, Query
from pydantic import UUID4
from datetime import datetime

from app.routers.consumption import consumption_req_schema, consumption_res_schema # noqa
from app.db.models.aqs_enums import aggregation_enum
from app.auth.permissions import authorize
from app.routers.consumption import consumption_crud
from app.routers.consumption.consumption_res_docs import total_csm, top_dwell
from app.auth import verify

router = APIRouter()


@router.get(
    "/consumption/{community_id}",
    status_code=status.HTTP_200_OK,
    response_model=consumption_res_schema.consumption_by_community,
    responses=total_csm.responses,

)
async def total_consumption(
    community_id: UUID4,
    start_date: datetime = Query(..., description="Start date in ISO format"),
    end_date: datetime = Query(..., description="End date in ISO format"),
    aggregation: aggregation_enum = Query(..., description="Aggregation type: month, week, or day"), # noqa
    user_token=Depends(verify.get_user_token),
):
    await authorize.user_is_superuser_or_admin(
        user_token,
    )

    if aggregation == aggregation_enum.day:
        response = await consumption_crud.daily_data(
            user_token=user_token,
            communityid=community_id,
            start_ist=start_date,
            end_ist=end_date,
        )

    if aggregation == aggregation_enum.week:
        response = await consumption_crud.weekly_data(
            user_token=user_token,
            communityid=community_id,
            start_ist=start_date,
            # end_ist=end_date,
        )

    if aggregation == aggregation_enum.month:
        response = await consumption_crud.monthly_data(
            user_token=user_token,
            communityid=community_id,
            start_ist=start_date,
        )

    return {**response}


@router.get(
    "/top-dwellings/{community_id}",
    status_code=status.HTTP_200_OK,
    response_model=consumption_res_schema.TopDwellingsConsumption,
    responses=top_dwell.responses,

)
async def top_dwellings(
    community_id: UUID4,
    start_date: datetime = Query(..., description="Start date in ISO format"),
    end_date: datetime = Query(..., description="End date in ISO format"),
    aggregation: aggregation_enum = Query(..., description="Aggregation type: month, week, or day"), # noqa
    user_token=Depends(verify.get_user_token),
):

    await authorize.user_is_superuser_or_admin(
        user_token
    )
    if aggregation == aggregation_enum.month:
        response = await consumption_crud.month_top_dwellings_consumption(
            user_token=user_token,
            communityid=community_id,
            start_ist=start_date,
            end_ist=end_date,
            aggregation=aggregation,

        )
    if aggregation == aggregation_enum.week:
        response = await consumption_crud.week_top_dwellings_consumption(
            user_token=user_token,
            communityid=community_id,
            start_ist=start_date,
            end_ist=end_date,
            aggregation=aggregation,

        )
    if aggregation == aggregation_enum.day:
        response = await consumption_crud.day_top_dwellings_consumption(
            user_token=user_token,
            communityid=community_id,
            start_ist=start_date,
            end_ist=end_date,
            aggregation=aggregation,

        )
    return response
