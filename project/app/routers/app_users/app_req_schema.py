from datetime import date
from typing import Optional
from enum import Enum
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


class user_status_enum(str, Enum):
    active = "active"
    inactive = "inactive"
    deleted = "deleted"


class roles_enum(str, Enum):
    owner = "owner"
    tenant = "tenant"
    family = "family"


class update_user_status(BaseModel):
    role: Optional[roles_enum] = roles_enum.owner
    user_status: Optional[user_status_enum] = user_status_enum.active
