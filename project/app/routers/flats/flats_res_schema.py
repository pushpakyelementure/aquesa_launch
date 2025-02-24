from pydantic import BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from typing import Optional

from app.db.models.app_user import roles

PhoneNumber.phone_format = "E164"


class read_flats(BaseModel):
    flat_no: str
    type_of: str
    role: Optional[roles] = roles.owner
    name: str
    email: EmailStr
    mobile:  PhoneNumber


class change_owner(BaseModel):
    detail: str


class create_tenant(BaseModel):
    detail: str


class update_tenant(BaseModel):
    detail: str