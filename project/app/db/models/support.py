from beanie import Document
from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, AnyUrl, UUID4
import os


class category_enum(str, Enum):
    web_app_issues = "web_app_issues"
    moblie_app_issues = "mobile_app_issues"
    valve_issues = "valve_issues"
    subcription = "subcription"
    other = "other"


class status_enum(str, Enum):
    New = "New"
    Active = "Active"
    Resolved = "Resolved"


class timeline_dict(BaseModel):
    name: str
    date: datetime
    description: Optional[str] = None
    document: Optional[List[AnyUrl]] = None


class meta_info(BaseModel):
    created_at: datetime
    created_by: str


class service_request(Document):
    sr_id: str
    community_id: UUID4
    dwelling_id: UUID4
    date: datetime
    category: Optional[category_enum]
    description: Optional[str] = None
    status: Optional[status_enum]
    documents: Optional[List[AnyUrl]] = None
    timeline: Optional[List[timeline_dict]] = None
    meta: meta_info

    class Settings:
        name = os.getenv("SERVICE_REQUEST_COLL")  # Collection name
        indexes = [
            "community_id",
            "dwelling_id",
            "sr_id",
        ]
