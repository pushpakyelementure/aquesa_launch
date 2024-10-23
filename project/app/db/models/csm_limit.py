import os
from beanie import Document
from pydantic import BaseModel, UUID4

from datetime import datetime
from typing import Optional


class activity_info(BaseModel):
    timestamp: datetime
    action_by: str


class day_limit(Document):
    dwelling_id: UUID4
    limit: Optional[int] = 0
    activity: activity_info

    class Settings:
        name = os.getenv("CONSUMPTION_DAY_LIMIT_COLL")
        indexes = [
            "dwelling_id",
        ]
