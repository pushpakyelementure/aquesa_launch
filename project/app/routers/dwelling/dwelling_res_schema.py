from datetime import datetime
from typing import List, Optional

from pydantic import UUID4, BaseModel

from app.db.models.dwelling import device_status, device_type_enum


class dwell_create(BaseModel):
    dwelling_id: UUID4
    detail: str


class activity_info(BaseModel):
    updated_by: str
    updated_at: datetime


class meta_data(BaseModel):
    ver: float
    created_by: Optional[str] = None
    created_at: Optional[datetime] = None
    activity: Optional[activity_info] = None


class device_list(BaseModel):
    device_id: UUID4
    device_type: Optional[device_type_enum]
    serial_no: str
    group: str
    tag: str
    customTag: List[str]
    status: Optional[device_status]


class dwell_read(BaseModel):
    community_id: UUID4
    dwelling_id: UUID4
    community_name: str
    block: str
    floor_no: str
    flat_no: str
    type_of: str
    time_zone: str
    devices: Optional[List[device_list]]
    meta: meta_data


class read_all(BaseModel):
    community_id: UUID4
    dwelling_id: UUID4
    community_name: str
    block: str
    floor_no: str
    flat_no: str
    type_of: str
    time_zone: str
    devices: Optional[List[device_list]]
