from fastapi import APIRouter, status, HTTPException, Depends
from typing import List
from pydantic import UUID4

from app.routers.notification import notification_crud
from app.routers.notification import notification_res_schema
from app.auth.permissions import authorize
from app.auth import verify


router = APIRouter()


@router.get(
    "/{community_id}",
    status_code=status.HTTP_200_OK,
    response_model=List[notification_res_schema.get_notification],
)
async def get_notifications(
    community_id: UUID4,
    user_token=Depends(verify.get_user_token)
):
    await authorize.user_is_superuser(
        user_token=user_token
        )
    try:
        community = await notification_crud.get_notify(community_id)
        print(community)
        return [{
            "community_id": community_id,
            "datetime": comm.datetime,
            "message": comm.message,
            "title": comm.title,
            "notification_type": comm.notification_type
        }for comm in community
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
