from typing import List, Optional

from pydantic import BaseModel

from app.db.models.dwelling import device_type_enum, device_status


class devices(BaseModel):
    device_type: device_type_enum
    serial_no: Optional[str] = None
    group: Optional[str] = None
    tag: Optional[str] = None
    customTag: Optional[List[str]] = None
    status: Optional[device_status]
