from datetime import datetime

from fastapi import HTTPException, status

from app.db.models.app_user import app_users_model
from app.db.models.community import community_model


async def create_app_user(**data):
    result = app_users_model(**data)
    await result.insert()


async def read_all_app_users(community_id):
    community = await community_model.find_one(
        community_model.community_id == community_id
    )
    if community is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Community Not found",
        )
    user = await app_users_model.find(app_users_model.dwelling["community_id"] == community_id).to_list() # noqa

    if user is None:
        raise HTTPException(
               status_code=status.HTTP_404_NOT_FOUND,
               detail="Users not found",
           )
    return user


async def read_one_app_user(user_id):
    user = await app_users_model.find_one(app_users_model.user_id == user_id)

    if user is None:
        raise HTTPException(
               status_code=status.HTTP_404_NOT_FOUND,
               detail="User not found",
           )
    return user


async def update_app_user_info(community_id, user_id, user_token, **data):
    community = await community_model.find_one(
        community_model.community_id == community_id
    )
    if community is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Community Not found",
        )
    user = await app_users_model.find_one(app_users_model.user_id == user_id)
    if user is None:
        raise HTTPException(
               status_code=status.HTTP_404_NOT_FOUND,
               detail="User not found",
           )
    user.name = data["name"]
    user.mobile = data["mobile"]
    user.email = data["email"]
    if "birth_date" in data:
        var = data["birth_date"]
        birthdate = datetime(var.year, var.month, var.day)
        iso_birth_date = birthdate.strftime("%Y-%m-%dT%H:%M:%SZ")
        user.birth_date = datetime.strptime(iso_birth_date, "%Y-%m-%dT%H:%M:%SZ") # noqa
    user.meta.activity = {
         "updated_by": user_token["uid"],
         "updated_at": datetime.utcnow(),
            }
    await user.save()
    return user


async def delete_app_user(user_id):
    del_user = await app_users_model.find_one(
        app_users_model.user_id == user_id,
    )
    if del_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # await del_user.update({"$set": {"user_status": "deleted"}})
    await del_user.delete()
    return del_user
