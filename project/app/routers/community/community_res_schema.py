from datetime import datetime
from typing import List, Optional

from pydantic import UUID4, BaseModel

from app.db.models.community import subscription_status_enum


class create_community(BaseModel):
    community_id: UUID4
    detail: str


class activity_info(BaseModel):
    updated_by: str
    updated_at: datetime


class meta(BaseModel):
    ver: float
    created_by: Optional[str] = None
    created_at: Optional[datetime] = None
    activity: Optional[activity_info] = None


class address_dict(BaseModel):
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]
    zip_code: Optional[str]
    time_zone: Optional[str]


class read_one(BaseModel):
    community_name: str
    location: address_dict
    dwelling_types: Optional[List[dict]] = None
    bill_model: Optional[str] = None
    billing_cycle_date: Optional[int] = None
    billing_start_date: Optional[datetime] = None
    next_invoice_date: datetime
    gst_no: Optional[str] = None
    subscription_status: Optional[subscription_status_enum]  # noqa
    meta: meta


class read_all(BaseModel):
    community_name: str
    location: address_dict
    dwelling_types: Optional[List[dict]] = None
    bill_model: Optional[str] = None
    billing_cycle_date: Optional[int] = None
    billing_start_date: Optional[datetime] = None
    next_invoice_date: datetime
    gst_no: Optional[str] = None
    subscription_status: Optional[subscription_status_enum]  # noqa


class meta_info(BaseModel):
    ver: float
    activity: activity_info


class update(BaseModel):
    community_name: str
    location: address_dict
    dwelling_types: Optional[List[dict]] = None
    bill_model: Optional[str] = None
    billing_cycle_date: Optional[int] = None
    billing_start_date: Optional[datetime] = None
    next_invoice_date: datetime
    gst_no: Optional[str] = None
    subscription_status: Optional[subscription_status_enum]  # noqa
    meta: meta_info


class patch_community(BaseModel):
    detail: str
    subscription_status: subscription_status_enum
    meta: meta_info
