import os
from pydantic import BaseModel, UUID4
from beanie import Document
from pymongo import IndexModel
from datetime import datetime
from enum import Enum

from typing import Optional


class valve_status_enum(str, Enum):
    open = "open"
    close = "close"


class activity_info(BaseModel):
    timestamp: datetime
    action_by: Optional[str] = None


class device_status(Document):
    device_id: Optional[UUID4]
    valve_status: Optional[valve_status_enum] = valve_status_enum.open
    tag: Optional[str] = None
    custom_tag: Optional[str] = None
    activity: Optional[activity_info] = None

    class Settings:
        name = os.getenv("VALVE_STATUS_COLL")
        indexes = [
            "device_id",
            IndexModel([("activity.action_by")]),
        ]
