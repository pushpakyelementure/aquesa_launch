from fastapi import HTTPException, status

from app.db.models.dwelling import dwelling_model
from app.db.models.app_user import roles
from app.db.models.app_user import app_users_model, user_status_enum


# Read a dwelling
async def get_by_dwelling(dwelling_id):
    dwell = await dwelling_model.find_one(dwelling_model.dwelling_id == dwelling_id) # noqa
    if dwell is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dwelling not found",
        )
    return dwell


# Change the ownership
async def post_by_dwelling(dwelling_id, **data_to_db):
    dwell = await app_users_model.find_one(app_users_model.dwelling.dwelling_id == dwelling_id) # noqa
    if dwell is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dwelling not found",
        )
    dwell.name = data_to_db["name"]
    dwell.mobile = data_to_db["mobile"]
    dwell.email = data_to_db["email"]

    await dwell.save()
    return dwell


# Add the tenant
async def add_tenant(dwelling_id, **data_to_db):
    dwell = await app_users_model.find_one(app_users_model.dwelling.dwelling_id == dwelling_id) # noqa
    if dwell is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dwelling not found",
        )
    for rol in dwell.dwelling:
        rol.role = roles.tenant

    # Update the dwelling fields
    dwell.name = data_to_db["name"]
    dwell.mobile = data_to_db["mobile"]
    dwell.email = data_to_db["email"]

    await dwell.save()
    return dwell


# Update the tenant
async def update_tenant(dwelling_id, **data_to_db):
    dwell = await app_users_model.find_one(app_users_model.dwelling.dwelling_id == dwelling_id) # noqa
    if dwell is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dwelling not found",
        )
    # Update the dwelling fields
    dwell.name = data_to_db["name"]
    dwell.mobile = data_to_db["mobile"]
    dwell.email = data_to_db["email"]

    await dwell.save()
    return dwell


# Delete a tenent
async def delete_tenant(dwelling_id):
    dwell = await app_users_model.find_one(app_users_model.dwelling.dwelling_id == dwelling_id)  # noqa
    if dwell is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="community not found",
        )
    for dwelling in dwell.dwelling:
        dwelling.user_status = user_status_enum.blocked
    await dwell.save()
    return None
