from beanie import Document
from pydantic import UUID4
from datetime import datetime
from enum import Enum
from typing import List
import os


class notification_enum(str, Enum):
    payment = "payment"
    water_measure = "water_measure"


class notifications(Document):
    community_id: UUID4
    datetime: datetime
    message: str
    title: str
    notification_type: List[notification_enum] = [notification_enum.payment] # noqa

    class Settings:
        name = os.getenv("NOTIFICATION_COLL")
        indexes = [
            "community_id",
        ]
