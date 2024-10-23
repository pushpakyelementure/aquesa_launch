from datetime import datetime

from fastapi import HTTPException, status

from app.db.models.community import community_model
from app.db.models.community_user import community_users_model


# Create a new community user information
async def create_comm_user(**data):
    # community = await community_model.find_one(
    #     community_model.community_id == community_id
    # )

    # if community is None:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="Community Not found",
    #     )
    result = community_users_model(**data)
    await result.insert()


# Read all community users information
async def read_comm_user(community_id):
    community = await community_model.find_one(
        community_model.community_id == community_id
    )

    if community is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Community Not found",
        )
    read_data = await community_users_model.find_all().to_list()
    if read_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Users not found",
        )
    return read_data


# Read a community user information
async def read_one_user(community_id, user_id):
    community = await community_users_model.find_one(
        community_users_model.community_id == community_id
    )
    if community is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Community Not found",
        )
    read_data = await community_users_model.find_one(community_users_model.user_id == user_id) # noqa
    if read_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Users not found",
        )
    return read_data


# Patch a community user contact information
async def update_comm_contact(community_id, user_id, user_token, **data):
    community = await community_users_model.find_one(
        community_users_model.community_id == community_id
    )
    if community is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Community Not found",
        )
    user = await community_users_model.find_one(community_users_model.user_id == user_id) # noqa
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    user.meta.activity = {
        "updated_by": user_token['uid'],
        "updated_at": datetime.utcnow(),
    }
    await user.update({"$set": {"meta.activity": user.meta.activity}})
    await user.update({"$set": {**data}})
    return user


# Upadet a community user information
async def update_comm_user(community_id, user_id, user_token, **data):
    community = await community_users_model.find_one(
        community_users_model.community_id == community_id
    )
    if community is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Community Not found",
        )
    user = await community_users_model.find_one(community_users_model.user_id == user_id) # noqa
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    if "role" in data:
        user.role = [data["role"]]
    user.name = data["name"]
    user.mobile = data["mobile"]
    user.email = data["email"]
    user.title = data["title"]
    user.user_status = data["user_status"]
    if "birth_date" in data:
        var = data["birth_date"]
        birthdate = datetime(var.year, var.month, var.day)
        iso_birth_date = birthdate.strftime("%Y-%m-%dT%H:%M:%SZ")
        user.birth_date = datetime.strptime(
            iso_birth_date, "%Y-%m-%dT%H:%M:%SZ"
        )  # noqa
    user.meta.activity = {
        "updated_by": user_token['uid'],
        "updated_at": datetime.utcnow(),
    }
    await user.save()
    return user


# Delete a community user change the user_status as deleted
async def delete_comm_user(user_id, community_id):
    comm = await community_users_model.find_one(
        community_users_model.community_id == community_id
    )
    if comm is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Community not found",
        )

    comm_user = await community_users_model.find_one(
        community_users_model.user_id == user_id,
    )
    if comm_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    await comm_user.update({"$set": {"user_status": "deleted"}})
    return comm_user
