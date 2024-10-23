from datetime import datetime

from fastapi import HTTPException, status

from app.db.models.admin_user import admin_user_model


async def create_admin_user(**data):
    result = admin_user_model(**data)
    await result.insert()


async def read_one_admin(user_id):
    user = await admin_user_model.find_one(admin_user_model.user_id == user_id)
    if user is None:
        raise HTTPException(
               status_code=status.HTTP_404_NOT_FOUND,
               detail="User not found",
           )
    return user


async def read_all_admin():
    user = await admin_user_model.find().to_list()

    if user is None:
        raise HTTPException(
               status_code=status.HTTP_404_NOT_FOUND,
               detail="Users not found",
           )
    return user


async def update_admin(user_id, user_token, **data):
    user = await admin_user_model.find_one(admin_user_model.user_id == user_id)
    if user is None:
        raise HTTPException(
               status_code=status.HTTP_404_NOT_FOUND,
               detail="Users not found",
           )
    if "role" in data:
        user.role = [data["role"]]
    user.name = data["name"]
    user.email = data["email"]
    user.mobile = data["mobile"]
    user.meta.activity = {
        "updated_by": user_token["uid"],
        "updated_at": datetime.utcnow()
    }
    await user.save()
    return user


async def update_admin_role(user_id, user_token, **data):
    user = await admin_user_model.find_one(admin_user_model.user_id == user_id)
    if user is None:
        raise HTTPException(
               status_code=status.HTTP_404_NOT_FOUND,
               detail="User not found",
           )
    user.meta.activity = {
         "updated_by": user_token["uid"],
         "updated_at": datetime.utcnow(),
            }
    if "role" in data:
        data["role"] = [data["role"]]
    await user.update({"$set": {"meta.activity": user.meta.activity}})
    await user.update({"$set": {**data}})
    return user


async def delete_admin_user(user_id):
    del_user = await admin_user_model.find_one(
        admin_user_model.user_id == user_id,
    )
    if del_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    await del_user.update({"$set": {"user_status": "deleted"}})
    return del_user
