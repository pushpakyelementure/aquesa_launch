from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import UUID4

from app.auth import manage, verify
from app.auth.permissions import authorize

from app.db.models.community import community_model
from app.routers.app_users import app_crud, app_req_schema, app_res_schema
from app.routers.app_users.app_users_res_doc import (  # Noqa
    create_app,
    delete_app,
    get_app,
    update_app,
)

router = APIRouter()


@router.get(
    "/{community_id}",
    response_model=List[app_res_schema.user_read_resp_model],
    status_code=status.HTTP_200_OK,
    responses=get_app.responses,
)
async def get_all_app_users(
    community_id: UUID4,
    user_token=Depends(verify.get_user_token),
):
    await authorize.user_is_superuser_or_admin(
        user_token,
    )
    try:
        read_all = await app_crud.read_all_app_users(community_id)
        return read_all
    except Exception as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get(
    "/{community_id}/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=app_res_schema.user_read_resp_model,
    responses=get_app.responses,
)
async def get_specific_app_user(
    community_id: UUID4,
    user_id: str,
    user_token=Depends(verify.get_user_token),
):
    await authorize.user_is_superuser_or_admin(
        user_token,
    )
    try:
        read_user = await app_crud.read_one_app_user(user_id)
        return {
            "user_id": user_id,
            "name": read_user.name,
            "mobile": read_user.mobile,
            "email": read_user.email,
            "birth_date": read_user.birth_date,
            "profile_picture": read_user.profile_picture,
            "dwelling": read_user.dwelling,
            "meta": read_user.meta,
        }
    except Exception as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.post(
    "/{community_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=app_res_schema.user_create_resp_model,
    responses=create_app.responses,
)
async def create_app_user(
    community_id: UUID4,
    req: app_req_schema.user_create,
    user_token=Depends(verify.get_user_token),
):
    await authorize.user_is_superuser_or_admin(
        user_token,
    )
    community = await community_model.find_one(
        community_model.community_id == community_id
    )
    if community is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Community Not found",
        )
    app_user_id = await manage.create_user_by_mobile(req.mobile)
    meta = {
        "ver": 1.0,
        "created_by": user_token["uid"],
        "created_at": datetime.utcnow(),
    }
    data = {
        "user_id": app_user_id,
        "name": req.name,
        "mobile": req.mobile,
        "email": req.email,
        "profile_picture": req.profile_picture,
        "birth_date": req.birth_date,
        "meta": meta,
    }
    try:
        await app_crud.create_app_user(**data)
        return {
            "user_id": app_user_id,
            "detail": "app user created",
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.put(
    "/{community_id}/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=app_res_schema.user_update_resp_model,
    responses=update_app.responses,
)
async def put_app_user(
    community_id: UUID4,
    user_id: str,
    req: app_req_schema.update_user,
    user_token=Depends(verify.get_user_token),
):
    await authorize.user_is_superuser_or_admin(
        user_token,
    )
    data = {
        "name": req.name,
        "mobile": req.mobile,
        "email": req.email,
        "birth_date": req.birth_date,
    }
    try:
        await app_crud.update_app_user_info(
            community_id, user_id, user_token, **data
        )  # noqa
        await manage.change_mobile_number(user_id, req.mobile)
        return {
            "user_id": user_id,
            "detail": "app user info updated successfully",
            "updated_info": data,
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


@router.patch(
    "/{dwelling_id}/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=app_res_schema.user_patch_resp_model,
    responses=update_app.responses,
)
async def update_dwell_info(
    dwelling_id: UUID4,
    user_id: str,
    req: app_req_schema.update_user_status,
    user_token=Depends(verify.get_user_token),
):
    await authorize.user_is_superuser_or_admin(
        user_token,
    )
    data = {
        "user_status": req.user_status,
        "role": req.role
    }
    try:
        await app_crud.update_app_user_status(
            dwelling_id, user_id, **data
        )  # noqa 
        return {
            "user_id": user_id,
            "detail": "app user info updated successfully",
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


@router.delete(
    "/{community_id}/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=delete_app.responses,
)
async def delete_app_user(
    community_id: UUID4,
    user_id: str,
    user_token=Depends(verify.get_user_token),
):
    await authorize.user_is_superuser_or_admin(
        user_token,
    )
    try:
        await app_crud.delete_app_user(user_id)
        return None
    except Exception as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
