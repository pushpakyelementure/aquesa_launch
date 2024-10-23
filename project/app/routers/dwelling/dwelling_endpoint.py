import uuid
from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import UUID4

from app.auth import verify
from app.auth.permissions import authorize
from app.db.models.community import community_model
from app.routers.dwelling import dwelling_crud, dwelling_req_schema, dwelling_res_schema # noqa
from app.routers.dwelling.dwelling_res_docs import (
    create_dwelling,
    delete_dwelling,
    read_dwelling,
    readall_dwelling,
    update_dwelling,
)

router = APIRouter()


# Read All the Dwelling documents using GET method
@router.get(
    "/community/{community_id}",
    status_code=status.HTTP_200_OK,
    response_model=List[dwelling_res_schema.read_all],
    responses=readall_dwelling.responses,
)
async def get_all_dwellings(
    community_id: UUID4,
    user_token=Depends(verify.get_user_token),
):
    await authorize.user_is_superuser_or_admin_or_support_or_field(
        user_token=user_token,
    )
    dwells = await dwelling_crud.get_dwelling_by_community(community_id)
    try:
        return [
            {
                "dwelling_id": dwell.dwelling_id,
                "community_id": dwell.community_id,
                "community_name": dwell.community_name,
                "flat_no": dwell.flat_no,
                "floor_no": dwell.floor_no,
                "block": dwell.block,
                "type_of": dwell.type_of,
                "time_zone": dwell.time_zone,
                "devices": dwell.devices,
            }
            for dwell in dwells
        ]

    except Exception as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


# Read a Dwelling document using GET method
@router.get(
    "/{dwelling_id}",
    status_code=status.HTTP_200_OK,
    response_model=dwelling_res_schema.dwell_read,
    responses=read_dwelling.responses,
)
async def get_dwelling_by_id(
    dwelling_id: UUID4,
    user_token=Depends(verify.get_user_token),
):
    await authorize.user_is_superuser_or_admin_or_support_or_field(
        user_token=user_token,
    )
    try:
        dwell = await dwelling_crud.get_dwelling_by_id(dwelling_id)
        return {
            "dwelling_id": dwell.dwelling_id,
            "community_id": dwell.community_id,
            "community_name": dwell.community_name,
            "flat_no": dwell.flat_no,
            "floor_no": dwell.floor_no,
            "block": dwell.block,
            "type_of": dwell.type_of,
            "time_zone": dwell.time_zone,
            "devices": dwell.devices,
            "meta": dwell.meta,
        }
    except Exception as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


# Create a Dwelling document using POST method
@router.post(
    "/community/{community_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=dwelling_res_schema.dwell_create,
    responses=create_dwelling.responses,
)
async def create_dwelling(
    community_id: UUID4,
    req: dwelling_req_schema.dwelling_create,
    user_token=Depends(verify.get_user_token),
):
    await authorize.user_is_superuser_or_admin(
            user_token=user_token,
    )
    community = await community_model.find_one(
        community_model.community_id == community_id
    )

    if community is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Community Not found",
        )
    data = {
        "community_id": community_id,
        "dwelling_id": str(uuid.uuid4()),
        "community_name": community.community_name,
        "flat_no": req.flat_no,
        "floor_no": req.floor_no,
        "block": req.block,
        "type_of": req.type_of,
        "time_zone": community.location.time_zone,
        "meta": {
            "ver": 1.0,
            "created_by": user_token["uid"],
            "created_at": datetime.utcnow(),
        },
    }
    try:
        await dwelling_crud.create_dwelling(user_token, **data)
        return {
            "dwelling_id": data["dwelling_id"],
            "detail": "Dwelling created successfully",
        }
    except Exception as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


# Update the Dwelling document using PATCH method
@router.patch(
    "/{dwelling_id}",
    status_code=status.HTTP_200_OK,
    response_model=dwelling_res_schema.dwell_read,
    responses=update_dwelling.responses,
)
async def change_dwelling_info(
    dwelling_id: UUID4,
    req: dwelling_req_schema.dwelling_update,
    user_token=Depends(verify.get_user_token),
):
    await authorize.user_is_superuser_or_admin(
        user_token=user_token,
    )
    data = {key: value for key, value in req.dict(exclude_unset=True).items()}

    try:
        dwell = await dwelling_crud.change_dwelling_info(
            dwelling_id, user_token, **data
        )  # noqa
        return {
            "dwelling_id": dwell.dwelling_id,
            "community_id": dwell.community_id,
            "community_name": dwell.community_name,
            "flat_no": dwell.flat_no,
            "floor_no": dwell.floor_no,
            "block": dwell.block,
            "type_of": dwell.type_of,
            "time_zone": dwell.time_zone,
            "devices": dwell.devices,
            "meta": dwell.meta,
        }
    except Exception as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


# Delete a Dwelling document using DELETE method
@router.delete(
    "/{dwelling_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=delete_dwelling.responses,
)
async def delete_dwelling(
    dwelling_id: UUID4,
    user_token=Depends(verify.get_user_token),
):
    await authorize.user_is_superuser_or_admin(
        user_token=user_token,
    )
    try:
        await dwelling_crud.delete_dwelling(dwelling_id)
        return None
    except Exception as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
