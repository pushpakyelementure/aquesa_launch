from datetime import date
from typing import Optional

from pydantic import AnyUrl, BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber

PhoneNumber.phone_format = "E164"


class user_create(BaseModel):
    name: Optional[str] = None
    mobile: PhoneNumber
    email: Optional[EmailStr] = None
    profile_picture: Optional[AnyUrl] = None
    birth_date: Optional[date] = None


class update_user(BaseModel):
    name: Optional[str] = None
    mobile: PhoneNumber
    email: Optional[EmailStr] = None
    birth_date: Optional[date] = None


class patch_user(BaseModel):
    name: Optional[str] = None
    birth_date: Optional[date] = None
    email: Optional[EmailStr] = None
