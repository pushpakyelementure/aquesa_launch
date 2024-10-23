from typing import Optional

from pydantic import BaseModel


class dwelling_create(BaseModel):
    block: Optional[str] = None
    floor_no: Optional[str] = None
    flat_no: Optional[str] = None
    type_of: Optional[str] = None


class dwelling_update(BaseModel):
    block: Optional[str] = None
    floor_no: Optional[str] = None
    flat_no: Optional[str] = None
    type_of: Optional[str] = None
