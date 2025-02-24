from pydantic import BaseModel, UUID4
from datetime import datetime
from typing import List

from app.db.models.notification import notification_enum


class get_notification(BaseModel):
    community_id: UUID4
    datetime: datetime
    message: str
    title: str
    notification_type: List[notification_enum]
