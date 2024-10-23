from typing import List

from pydantic import UUID4, BaseModel

from app.db.models.dwelling import device_status, device_type_enum


class create_device(BaseModel):
    detail: str


class devices(BaseModel):
    device_id: UUID4
    device_type: device_type_enum
    serial_no: str
    group: str
    tag: str
    customTag: List[str]
    status: device_status


class update_device(BaseModel):
    detail: str
