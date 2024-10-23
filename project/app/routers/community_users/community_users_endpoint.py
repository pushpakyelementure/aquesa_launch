from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import UUID4

from app.auth import manage, verify
from app.auth.genpass import hash_password
from app.auth.permissions import authorize
from app.db.models.community import community_model
from app.routers.community_users import community_users_crud  # noqa
from app.routers.community_users import (community_users_req_schema, community_users_res_schema) # noqa
from app.routers.community_users.community_users_res_docs import (
    create_community_users, delete_community_users, get_community_users,
    get_single_community_users, update_community_users,
    update_community_user_contact)

router = APIRouter()


# Read All community users using GET method
@router.get(
    "/{community_id}",
    status_code=status.HTTP_200_OK,
    response_model=List[community_users_res_schema.read_user],
    responses=get_community_users.responses,
)
async def get_community_users(
    community_id: UUID4,
    user_token=Depends(verify.get_user_token),

):
    await authorize.user_is_superuser_or_admin(
        user_token,
    )
    try:
        comm_user = await community_users_crud.read_comm_user(community_id)
        return comm_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


# Read a community user using GET method
@router.get(
    "/{community_id}/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=community_users_res_schema.read_user,
    responses=get_single_community_users.responses
)
async def get_specific_community_user(
    community_id: UUID4,
    user_id: str,
    user_token=Depends(verify.get_user_token),

):
    await authorize.user_is_superuser_or_admin(
        user_token,
    )
    try:
        comm_user = await community_users_crud.read_one_user(community_id, user_id)  # noqa
        return comm_user
    except Exception as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


# Create a community user information using POST method
@router.post(
    "/{community_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=community_users_res_schema.create_res_model,
    responses=create_community_users.responses,
)
async def create_community_user(
    community_id: UUID4,
    req: community_users_req_schema.user_create,
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
    user_id = await manage.create_user(req.email, req.password)

    meta = {
        "ver": 1.0,
        "created_by": user_token['uid'],
        "created_at": datetime.utcnow(),
    }
    data_to_db = {
        "user_id": user_id,
        "community_id": community_id,
        "name": req.name,
        "mobile": req.mobile,
        "title": req.title,
        "email": req.email,
        "password": await hash_password(req.password),
        "birth_date": req.birth_date,
        "role": [req.role],
        "user_status": req.user_status,
        "meta": meta,
    }
    # Create a community user
    try:
        await community_users_crud.create_comm_user(**data_to_db)
        return {
            "community_id": community_id,
            "user_id": user_id,
            "detail": "Community_user created successfully",
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


# Update a community user contact detail using PATCH method
@router.patch(
    "/{community_id}/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=community_users_res_schema.update_comm_contact,
    responses=update_community_user_contact.responses,
)
async def patch_community_user(
    community_id: UUID4,
    user_id: str,
    req: community_users_req_schema.update_comm_contact,
    user_token=Depends(verify.get_user_token),

):
    await authorize.user_is_superuser_or_admin(
        user_token,
    )
    data = {key: value for key, value in req.dict(exclude_unset=True).items()}  # noqa
    try:
        await community_users_crud.update_comm_contact(
            community_id, user_id, user_token, **data,
        )
        return {
            "community_id": community_id,
            "user_id": user_id,
            "updated_details": data,
            "detail": " Updated successfully",
            "meta": {
                    "ver": 1.0,
                    "activity": {
                        "updated_by": user_token['uid'],
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


# Update a community user all information using PUT method
@router.put(
    "/{community_id}/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=community_users_res_schema.resp_comm_user,
    responses=update_community_users.responses
)
async def put_community_user(
    community_id: UUID4,
    user_id: str,
    req: community_users_req_schema.update_comm_user,
    user_token=Depends(verify.get_user_token),

):
    await authorize.user_is_superuser_or_admin(
        user_token,
    )
    data = {
        "name": req.name,
        "mobile": req.mobile,
        "email": req.email,
        "title": req.title,
        "birth_date": req.birth_date,
        "role": req.role,
        "user_status": req.user_status
    }
    try:
        await community_users_crud.update_comm_user(community_id, user_id, user_token, **data)  # noqa
        return {
                "community_id": community_id,
                "user_id": user_id,
                "updated_info": data,
                "meta": {
                    "ver": 1.0,
                    "activity": {
                        "updated_by": user_token['uid'],
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


# Delete a community user for change user_status as deleted using DETETE method
@router.delete(
    "/{community_id}/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=delete_community_users.responses,
)
async def delete_community_user(
    community_id: UUID4,
    user_id: str,
    user_token=Depends(verify.get_user_token),

):
    await authorize.user_is_superuser_or_admin(
        user_token,
    )
    try:
        await community_users_crud.delete_comm_user(user_id, community_id)  # noqa
        return None
    except Exception as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )
