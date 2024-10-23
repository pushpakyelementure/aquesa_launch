from datetime import datetime

from fastapi import HTTPException, status

from app.db.models.dwelling import dwelling_model
from app.db.models.csm_limit import day_limit


# Create a dwelling document
async def create_dwelling(user_token, **data_to_db):
    data = dwelling_model(**data_to_db)

    # limit for dwell
    activity_info = {
                  "timestamp": datetime.now(),
                  "action_by": user_token['uid'],
                 }
    dwell_limit = {
                       "dwelling_id": data_to_db['dwelling_id'],
                       "limit": 200,
                       "activity": activity_info
                      }
    limit_db = day_limit(**dwell_limit)
    await limit_db.insert()
    await data.insert()


# Readall the dwelling documnets
async def get_dwelling_by_community(community_id):
    comm = await dwelling_model.find_one(dwelling_model.community_id == community_id) # noqa
    if comm is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Community not found",
        )
    dwells = await dwelling_model.find(dwelling_model.community_id == community_id).to_list()  # noqa

    if dwells is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="community not found",
        )
    return dwells


# Read a dwelling documnet
async def get_dwelling_by_id(dwelling_id):
    dwell = await dwelling_model.find_one(dwelling_model.dwelling_id == dwelling_id) # noqa

    if dwell is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="dwelling not found",
        )
    return dwell


# Patch method for change the dwelling information
async def change_dwelling_info(dwelling_id, user_token, **data):

    dwell = await dwelling_model.find_one(
        dwelling_model.dwelling_id == dwelling_id,
    )
    if dwell is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dwelling not found",
            )
    dwell.meta.activity = {
         "updated_by": user_token["uid"],
         "updated_at": datetime.utcnow(),
            }
    await dwell.update({"$set": {"meta.activity": dwell.meta.activity}})
    await dwell.update({"$set": {**data}})

    return dwell


# Delete a dwelling document
async def delete_dwelling(dwelling_id):
    dwell = await dwelling_model.find_one(
        dwelling_model.dwelling_id == dwelling_id,
    )
    if dwell is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dwelling not found",
        )
    await dwell.delete()

    return None
