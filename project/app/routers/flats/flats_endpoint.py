from fastapi import APIRouter, status, HTTPException, Depends
from pydantic import UUID4

from app.auth import verify
from app.auth.permissions import authorize
from app.routers.flats import flats_res_schema, flats_req_schema, flats_crud
from app.db.models.app_user import app_users_model
# from app.routers.flats.flats_docs_res import (
#     get_flats,
#     delete_tenant,
#     post_owner,
#     post_tenant,
#     put_tenant
# )
router = APIRouter()


# Read the Flats details
@router.get(
    "/{dwelling_id}",
    status_code=status.HTTP_200_OK,
    response_model=flats_res_schema.read_flats,
    # responses=get_flats.responses
)
async def get_flat_details(
    dwelling_id: UUID4,
    user_token=Depends(verify.get_user_token),
):
    await authorize.user_is_superuser(
        user_token=user_token,
    )
    try:
        user = await app_users_model.find_one(app_users_model.dwelling.dwelling_id == dwelling_id) # noqa
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="user not found",
            )
        for i in user.dwelling:
            pass

        dwell = await flats_crud.get_by_dwelling(dwelling_id)
        return {
            "flat_no": dwell.flat_no,
            "type_of": dwell.type_of,
            "role": i.role,
            "name": user.name,
            "email": user.email,
            "mobile": user.mobile,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


# change flat ownership
@router.post(
    "/{dwelling_id}/owner",
    status_code=status.HTTP_201_CREATED,
    response_model=flats_res_schema.change_owner,
    # responses=post_owner.responses,

    )
async def change_ownership(
    dwelling_id: UUID4,
    req: flats_req_schema.change_owner,
    user_token=Depends(verify.get_user_token),

):
    await authorize.user_is_superuser(
        user_token=user_token,
    )
    data = {
        "name": req.name,
        "mobile": req.mobile,
        "email": req.email,
    }
    try:
        await flats_crud.post_by_dwelling(dwelling_id, **data)
        return {
            "detail": "Changed ownership of dwelling",
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


# Add a new tenent for flats
@router.post(
    "/{dwelling_id}/",
    status_code=status.HTTP_201_CREATED,
    response_model=flats_res_schema.create_tenant,
    # responses=post_tenant.responses,
    )
async def add_tenant(
    dwelling_id: UUID4,
    req: flats_req_schema.create_tenant,
    user_token=Depends(verify.get_user_token),
):
    await authorize.user_is_superuser(
        user_token=user_token,
    )
    data = {
        "name": req.name,
        "mobile": req.mobile,
        "email": req.email,
    }
    try:
        await flats_crud.add_tenant(dwelling_id, **data)
        return {
            "detail": "Add tenent for dwelling",
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


# Update the tenent info
@router.put(
    "/{dwelling_id}/tenent",
    status_code=status.HTTP_200_OK,
    response_model=flats_res_schema.update_tenant,
    # responses=put_tenant.responses,
    )
async def update_tenant(
    dwelling_id: UUID4,
    req: flats_req_schema.update_tenant,
    user_token=Depends(verify.get_user_token),
):
    await authorize.user_is_superuser(
        user_token=user_token,
    )
    data = {
        "name": req.name,
        "mobile": req.mobile,
        "email": req.email,
    }
    try:
        await flats_crud.update_tenant(dwelling_id, **data)
        return {
            "detail": "Changed tenent of dwelling",
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


# delete the tenant as marked as blocked
@router.delete(
    "/{dwelling_id}/tenant",
    status_code=status.HTTP_204_NO_CONTENT,
    # responses=delete_tenant.responses,
)
async def remove_tenant(
    dwelling_id: UUID4,
    user_token=Depends(verify.get_user_token),
):
    await authorize.user_is_superuser(
        user_token=user_token,
    )
    try:
        await flats_crud.delete_tenant(dwelling_id)
        return None
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
