from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from app.db.models.community import subscription_status_enum


class address_dict(BaseModel):
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    zip_code: Optional[str] = None
    time_zone: Optional[str] = None


class community_info(BaseModel):
    community_name: str
    location: address_dict
    dwelling_types: Optional[List[dict]] = None
    bill_model: Optional[str] = None
    billing_cycle_date: Optional[int] = None
    billing_start_date: Optional[datetime] = None
    next_invoice_date: Optional[datetime] = None
    gst_no: Optional[str] = None
    subscription_status: Optional[subscription_status_enum]  # noqa


class patch_community(BaseModel):
    subscription_status: Optional[subscription_status_enum] = None
