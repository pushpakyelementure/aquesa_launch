from fastapi import APIRouter, HTTPException, status, Depends, Query
from pydantic import UUID4
from datetime import datetime, timedelta
from bson import Binary

from app.auth import verify
from app.auth.permissions import authorize
from app.routers.dashboard import dashboard_res_schema, dashboard_crud
from app.db.models.app_user import app_users_model
from app.db.models.dwelling import dwelling_model
from app.db.models.consumption import rawdata
from app.db.models.aqs_enums import aggregation_enum
from app.routers.dashboard.dashboard_res_docs import block_wise_csm, info_of_comm, water_usage
from collections import defaultdict

router = APIRouter()


@router.get(
    "/{community_id}",
    status_code=status.HTTP_200_OK,
    response_model=dashboard_res_schema.get_info_of_community,
    responses=info_of_comm.responses,
)
async def retrieve_all_statistical_info_of_community(
    community_id: UUID4,
    user_token=Depends(verify.get_user_token),

):
    await authorize.user_is_superuser(
        user_token=user_token,
    )
    try:
        dwell = await dashboard_crud.get_community_info_by_id(community_id)
        flat_users = await app_users_model.find(app_users_model.dwelling.community_id == community_id).to_list() # noqa
        owner = 0
        tenant = 0
        for dwel in flat_users:
            for user in dwel.dwelling:
                if user.role == "owner":
                    owner += 1
                elif user.role == "tenant":
                    tenant += 1

        dev = 0
        for i in dwell:
            if i.devices:
                dev = dev+len(i.devices)
        roles = {
            "owners": owner,
            "tenants": tenant,
        }
        return {
            "community_id": community_id,
            "Total_Flats": len(dwell),
            "Total_Devices": dev,
            "Residence_Distribution": roles
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get(
    "/tower/{community_id}",
    status_code=status.HTTP_200_OK,
    response_model=dashboard_res_schema.BlockConsumption,
    responses=block_wise_csm.responses,
    )
async def blockwise_daily_data(
    community_id: UUID4,
    start_date: datetime = Query(..., description="Start date in ISO format"),
    end_date: datetime = Query(..., description="End date in ISO format"),
    user_token=Depends(verify.get_user_token),
):
    await authorize.user_is_superuser_or_admin(
        user_token
    )
    response = await dashboard_crud.block_data(
            user_token=user_token,
            community_id=community_id,
            start_ist=start_date,
            end_ist=end_date
    )
    return response


@router.get(
    "/water_usage/{community_id}",
    status_code=status.HTTP_200_OK,
    response_model=dashboard_res_schema.water_usage_Consumption,
    responses=water_usage.responses,
    )
async def water_usage(
    community_id: UUID4,
    start_date: datetime = Query(..., description="Start date in ISO format"),
    end_date: datetime = Query(..., description="End date in ISO format"),
    aggregation: aggregation_enum = Query(..., description="Aggregation type: month, week, or day"), # noqa
    user_token=Depends(verify.get_user_token),
):
    await authorize.user_is_superuser_or_admin(
        user_token
    )
    if aggregation == aggregation_enum.day:
        response = await dashboard_crud.water_usage_day(
            user_token=user_token,
            community_id=community_id,
            start_ist=start_date,
            end_ist=end_date,
        )

    if aggregation == aggregation_enum.week:
        response = await dashboard_crud.water_usage_week(
            user_token=user_token,
            community_id=community_id,
            start_ist=start_date,
        
        )

    if aggregation == aggregation_enum.month:
        response = await dashboard_crud.water_usage_month(
            user_token=user_token,
            community_id=community_id,
            start_ist=start_date,
        )

    return {**response}
