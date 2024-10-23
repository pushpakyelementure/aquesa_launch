from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.auth import manage, verify
from app.auth.genpass import hash_password
from app.auth.permissions import authorize
from app.routers.admin import admin_crud, admin_req_schema, admin_res_schema
from app.routers.admin.admin_res_docs import (  # Noqa
    create_admin,
    delete_admin,
    get_admin,
    patch_admin,
    update_admin,
)

router = APIRouter()


@router.get(
    "/",
    response_model=List[admin_res_schema.read_admin_user],
    status_code=status.HTTP_200_OK,
    responses=get_admin.responses,
)
async def get_all_admin_users(
    user_token=Depends(verify.get_user_token),
):
    await authorize.user_is_superuser(
        user_token,
    )
    try:
        read_all = await admin_crud.read_all_admin()
        return read_all
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get(
    "/{user_id}",
    response_model=admin_res_schema.read_admin_user,
    status_code=status.HTTP_200_OK,
    responses=get_admin.responses,
)
async def get_specific_admin_user(
    user_id: str,
    user_token=Depends(verify.get_user_token),
):
    await authorize.user_is_superuser(
        user_token,
    )
    try:
        read_user = await admin_crud.read_one_admin(user_id)
        return {
            "user_id": read_user.user_id,
            "employee_id": read_user.employee_id,
            "name": read_user.name,
            "mobile": read_user.mobile,
            "email": read_user.email,
            "role": read_user.role,
        }
    except Exception as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.post(
    "/",
    response_model=admin_res_schema.create_res_model,
    status_code=status.HTTP_201_CREATED,
    responses=create_admin.responses,
)
async def create_admin_user(
    req: admin_req_schema.admin_user_create,
    user_token=Depends(verify.get_user_token),
):
    await authorize.user_is_superuser(
        user_token,
    )

    admin_user_id = await manage.create_user(req.email, req.password)
    meta = {
        "ver": 1.0,
        "created_by": user_token["uid"],
        "created_at": datetime.utcnow(),
    }
    data = {
        "user_id": admin_user_id,
        "name": req.name,
        "employee_id": req.employee_id,
        "mobile": req.mobile,
        "email": req.email,
        "password": await hash_password(req.password),
        "role": [req.role],
        "user_status": req.user_status,
        "meta": meta,
    }
    try:
        await admin_crud.create_admin_user(**data)
        return {"user_id": admin_user_id, "detail": "admin user created"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.put(
    "/{user_id}",
    response_model=admin_res_schema.resp_update_comm_user,
    status_code=status.HTTP_200_OK,
    responses=update_admin.responses,
)
async def update_admin_user(
    user_id: str,
    req: admin_req_schema.update_admin_user,
    user_token=Depends(verify.get_user_token),
):
    await authorize.user_is_superuser(
        user_token,
    )
    data = {
        "name": req.name,
        "mobile": req.mobile,
        "email": req.email,
        "role": req.role,
    }
    try:
        await admin_crud.update_admin(user_id, user_token, **data)
        return {
            "user_id": user_id,
            "updated_info": data,
            "meta": {
                "activity": {
                    "updated_by": user_token["uid"],
                    "updated_at": datetime.utcnow(),
                }
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
    "/{user_id}",
    response_model=admin_res_schema.user_role_change,
    status_code=status.HTTP_200_OK,
    responses=patch_admin.responses,
)
async def change_role_of_user(
    user_id: str,
    req: admin_req_schema.update_admin_user_role,
    user_token=Depends(verify.get_user_token),
):
    await authorize.user_is_superuser(
        user_token,
    )
    data = {key: value for key, value in req.dict(exclude_unset=True).items()}  # noqa
    try:
        await admin_crud.update_admin_role(user_id, user_token, **data)
        return {"user_id": user_id, "detail": "user role changed"}
    except Exception as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=delete_admin.responses,
)
async def delete_admin_user(
    user_id: str,
    user_token=Depends(verify.get_user_token),
):
    await authorize.user_is_superuser(
        user_token,
    )
    try:
        await admin_crud.delete_admin_user(user_id)
        return None
    except Exception as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
