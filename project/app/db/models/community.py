import os
from beanie import Document
from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, UUID4


class address_dict(BaseModel):
    address: Optional[str]
    city: str
    state: str
    country: str
    zip_code: str
    time_zone: str


class subscription_status_enum(str, Enum):
    active = "active"
    inactive = "inactive"


class activity_info(BaseModel):
    updated_by: str
    updated_at: datetime


class meta_data(BaseModel):
    ver: float
    created_by: Optional[str] = None
    created_at: Optional[datetime] = None
    activity: Optional[activity_info] = None


class community_model(Document):
    community_id: UUID4
    community_name: str
    location: address_dict
    dwelling_types: list[dict]
    bill_model: str
    billing_cycle_date: int
    billing_start_date: datetime
    next_invoice_date: datetime
    gst_no: str
    subscription_status: Optional[subscription_status_enum] = (
        subscription_status_enum.inactive
    )  # noqa
    meta: meta_data

    class Settings:
        name = os.getenv("COMMUNITY_COLL")
        indexes = [
            "community_id",
            "community_name",
        ]
