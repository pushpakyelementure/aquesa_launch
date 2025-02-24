from pydantic import BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from typing import Optional

PhoneNumber.phone_format = "E164"


class change_owner(BaseModel):
    name: Optional[str] = None
    mobile: PhoneNumber
    email: EmailStr


class create_tenant(BaseModel):
    name: Optional[str] = None
    mobile: PhoneNumber
    email: EmailStr


class update_tenant(BaseModel):
    name: Optional[str] = None
    mobile: PhoneNumber
    email: EmailStr
