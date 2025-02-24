from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional, List
from datetime import datetime
from pydantic import UUID4


from app.routers.billing import billing_req_schema
from app.routers.billing import billing_res_schema
from app.routers.billing import billing_crud
from app.auth.permissions import authorize
from app.auth import verify


router = APIRouter()


@router.get(
    "/setup/{community_id}",
    response_model=List[billing_res_schema.bill_setup_comm_res]
     )
async def get_billing_setup(
    community_id: UUID4,
    user_token=Depends(verify.get_user_token),
     ):
    await authorize.user_is_superuser(
        user_token=user_token
        )
    try:
        comm_bill_setup = await billing_crud.read_comm_setup(community_id=community_id) # noqa
        # Get all the billing setup for the community
        # Logic to retrieve billing setup
        return comm_bill_setup
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.post(
    "/setup/{community_id}",
    response_model=billing_res_schema.bill_create_res,
    )
async def create_billing_setup(
    community_id: UUID4,
    req: billing_req_schema.bill_create_req,
    user_token=Depends(verify.get_user_token),
     ):
    await authorize.user_is_superuser(
        user_token=user_token,
        )
    # Billing setup for a community
    # Logic to create billing setup
    data = {
        #    "community_id": community_id,
           "year": req.year,
           "month": req.month,
           "fixed_cost": req.fixed_cost,
           "variable_cost": req.variable_cost,
           "bill_date": datetime.today().date(),
           }
    try:
        await billing_crud.comm_bill_setup(community_id, **data)
        return {
                "community_id": community_id,
                "detail": "community bill setup created successfully",
               }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.put(
    "/setup/{community_id}/{year}/{month}",
    response_model=billing_res_schema.update_bill_info)
async def update_billing_setup(
    community_id: UUID4,
    year: int,
    month: int,
    req: billing_req_schema.bill_update_req,
    user_token=Depends(verify.get_user_token),
):
    await authorize.user_is_superuser(
        user_token=user_token,
        )
    data = {
        "year": req.year,
        "month": req.month,
        "fixed_cost": req.fixed_cost,
        "variable_cost": req.variable_cost,
        "bill_date": req.bill_date
            }
    try:
        await billing_crud.update_comm_bill_setup(community_id, **data)  # noqa
        # Update billing setup
        # Logic to update billing setup for the given month
        return {
            "detail": " Updated successfully",
            "updated_info": data,
            "meta": {
                    "ver": 1.0,
                    "activity": {
                        "updated_by": user_token["uid"],
                        "updated_at": datetime.utcnow(),
                        },
                    },
                }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.post("/setup/{month}/publish")
async def publish_billing_setup(month: int):
    # Finalizing the billing setup and publising to consumers
    # Logic to finalize and publish billing setup
    return {
        "month": month,
        "message": "Billing setup published",
    }


@router.get("{dwelling_id}")
async def get_bills(
    dwelling_id: str,
    month: Optional[int] = None,
):
    # Get all the bills or a specific month bill for
    # the particular dwelling of a community
    # Logic to retrieve bills for the dwelling,
    # for all months or a specific month
    return {
        "dwelling_id": dwelling_id,
        "month": month,
        "bills": "Bill details",
    }


@router.get("{billing_id}/download")
async def download_bill(billing_id: UUID4):
    # Download the specific bill
    # Logic to download the specific bill
    return {
        "billing_id": billing_id,
        "message": "Download link or bill data",
    }
