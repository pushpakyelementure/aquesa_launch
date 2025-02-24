import os
from beanie import Document
from pydantic import UUID4,BaseModel
from datetime import datetime
from typing import Optional

from enum import Enum


class leakege(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    no_leakage = "no_leakage"


class alert_model(Document):
    device_id: UUID4
    timestamp: datetime
    alert: Optional[leakege] = leakege.no_leakage
    message: str


    class Settings:
        name = os.getenv("ALERTS_COLL")
        indexes = [
            "device_id"
        ]
