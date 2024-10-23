import uuid
from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import UUID4

from app.auth import verify
from app.auth.permissions import authorize
from app.routers.community import (
    community_crud,
    community_req_schema,
    community_res_schema,
)
from app.routers.community.community_res_docs import (
    create_community,
    delete_community,
    get_community,
    patch_community,
    update_community,
)

router = APIRouter()


# Read all Community documents Response Status code is 200
@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[community_res_schema.read_all],
    responses=get_community.responses,
)
async def get_all_community(
    user_token=Depends(verify.get_user_token),
):
    await authorize.user_is_superuser_or_admin_or_support(
        user_token=user_token,
    )
    try:
        community_data = await community_crud.get_all_community()
        return community_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# Read a Community document Response Status code is 200
@router.get(
    "/{community_id}",
    status_code=status.HTTP_200_OK,
    response_model=community_res_schema.read_one,
    responses=get_community.responses,
)
async def get_specific_community(
    community_id: UUID4,
    user_token=Depends(verify.get_user_token),
):
    await authorize.user_is_superuser_or_admin_or_support(
        user_token=user_token,
    )
    try:
        comm = await community_crud.get_community_by_id(community_id)
        return {
            "community_name": comm.community_name,
            "location": comm.location,
            "dwelling_types": comm.dwelling_types,
            "bill_model": comm.bill_model,
            "billing_cycle_date": comm.billing_cycle_date,
            "billing_start_date": comm.billing_start_date,
            "next_invoice_date": comm.next_invoice_date,
            "gst_no": comm.gst_no,
            "subscription_status": comm.subscription_status,
            "meta": comm.meta,
        }
    except Exception as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


# Create a community document information Response Status code is 201
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=community_res_schema.create_community,
    responses=create_community.responses,
)
async def create_community(
    req: community_req_schema.community_info,
    user_token=Depends(verify.get_user_token),
):
    await authorize.user_is_superuser_or_admin(
        user_token=user_token,
    )
    try:
        location = {
            "address": req.location.address,
            "city": req.location.city,
            "state": req.location.state,
            "country": req.location.country,
            "zip_code": req.location.zip_code,
            "time_zone": req.location.time_zone,
        }

        data_to_db = {
            "community_id": str(uuid.uuid4()),
            "community_name": req.community_name,
            "location": location,
            "dwelling_types": req.dwelling_types,
            "bill_model": req.bill_model,
            "billing_cycle_date": req.billing_cycle_date,
            "billing_start_date": req.billing_start_date,
            "next_invoice_date": req.next_invoice_date,
            "gst_no": req.gst_no,
            "subscription_status": req.subscription_status,
            "meta": {
                "ver": 1.0,
                "created_by": user_token["uid"],
                "created_at": datetime.utcnow(),
            },
        }
        await community_crud.create_community(**data_to_db)

        return {
            "community_id": data_to_db["community_id"],
            "detail": "Community created successfully",
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


# Update a community document information Response Status code is 200
@router.put(
    "/{community_id}",
    response_model=community_res_schema.update,
    status_code=status.HTTP_200_OK,
    responses=update_community.responses,
)
async def update_community(
    community_id: UUID4,
    req: community_req_schema.community_info,
    user_token=Depends(verify.get_user_token),
):
    await authorize.user_is_superuser_or_admin(
        user_token=user_token,
    )
    data = {
        "community_name": req.community_name,
        "location": dict(req.location),
        "dwelling_types": req.dwelling_types,
        "bill_model": req.bill_model,
        "billing_cycle_date": req.billing_cycle_date,
        "billing_start_date": req.billing_start_date,
        "next_invoice_date": req.next_invoice_date,
        "gst_no": req.gst_no,
        "subscription_status": req.subscription_status,
        "meta": {
            "ver": 1.0,
            "activity": {
                "updated_by": user_token["uid"],
                "updated_at": datetime.utcnow(),
            },
        },
    }
    try:
        await community_crud.update_community(community_id, **data)
        return {
            "community_name": data["community_name"],
            "location": data["location"],
            "dwelling_types": data["dwelling_types"],
            "bill_model": data["bill_model"],
            "billing_cycle_date": data["billing_cycle_date"],
            "billing_start_date": data["billing_start_date"],
            "next_invoice_date": data["next_invoice_date"],
            "gst_no": data["gst_no"],
            "subscription_status": data["subscription_status"],
            "meta": {
                "ver": 1.0,
                "activity": {
                    "updated_by": user_token["uid"],
                    "updated_at": datetime.utcnow(),
                },
            },
        }
    except Exception as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


# patch for change the subscription status [active or inactive]
@router.patch(
    "/{community_id}",
    response_model=community_res_schema.patch_community,
    status_code=status.HTTP_200_OK,
    responses=patch_community.responses,
)
async def change_subscription_status(
    community_id: UUID4,
    req: community_req_schema.patch_community,
    user_token=Depends(verify.get_user_token),
):
    await authorize.user_is_superuser_or_admin(
        user_token=user_token,
    )
    data = {key: value for key, value in req.dict(exclude_unset=True).items()}

    try:
        comm = await community_crud.subscription_status(
            community_id, user_token, **data
        )  # noqa

        return {
            "detail": "Changed Subscription status",
            "subscription_status": comm.subscription_status,
            "meta": comm.meta,
        }
    except Exception as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


# Delete a community document information Response Status code is 204
@router.delete(
    "/{community_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=delete_community.responses,
)
async def delete_community(
    community_id: UUID4,
    user_token=Depends(verify.get_user_token),
):
    await authorize.user_is_superuser_or_admin(
        user_token=user_token,
    )
    try:
        await community_crud.delete_community(community_id)
        return None
    except Exception as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
