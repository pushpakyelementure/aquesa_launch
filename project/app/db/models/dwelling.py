import os
from datetime import datetime
from enum import Enum
from typing import List, Optional

from beanie import Document
from pydantic import UUID4, BaseModel
from pymongo import IndexModel


class device_status(str, Enum):
    active = "active"
    inactive = "inactive"
    deleted = "deleted"


class device_type_enum(str, Enum):
    water_measure_mechanical = "water_measure_mechanical"
    water_quality = "water_quality"
    water_measure_ultra_sonic = "water_measure_ultra_sonic"


class device_list(BaseModel):
    device_id: UUID4
    device_type: Optional[device_type_enum] = device_type_enum.water_measure_mechanical # noqa
    serial_no: str
    group: str
    tag: Optional[str]
    customTag: Optional[List[str]]
    status: Optional[device_status] = device_status.active


class activity_info(BaseModel):
    updated_by: str
    updated_at: datetime


class meta_data(BaseModel):
    ver: float
    created_by: Optional[str] = None
    created_at: Optional[datetime] = None
    activity: Optional[activity_info] = None


class dwelling_model(Document):
    community_id: UUID4
    dwelling_id: UUID4
    community_name: str
    block: Optional[str] = None
    floor_no: str
    flat_no: str
    type_of: str
    time_zone: str
    devices: Optional[List[device_list]] = None
    meta: meta_data

    class Settings:
        name = os.getenv("DWELLING_COLL")
        indexes = [
            "community_id",
            "dwelling_id",
            IndexModel([("devices.device_id")]),
            IndexModel([("devices.serial_no")]),
        ]
