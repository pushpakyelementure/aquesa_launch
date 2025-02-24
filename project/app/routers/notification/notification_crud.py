from fastapi import HTTPException, status

from app.db.models.notification import notifications


async def get_notify(community_id):
    comm = await notifications.find_one(notifications.community_id == community_id) # noqa
    # print(comm)
    if comm is None:
        raise HTTPException(
               status_code=status.HTTP_404_NOT_FOUND,
               detail="Community not found",
           )
    notify = await notifications.find(notifications.community_id == community_id).to_list() # noqa
    return notify