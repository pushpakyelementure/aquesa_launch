import os
from datetime import date, datetime
from enum import Enum
from typing import List, Optional

from beanie import Document
from pydantic import UUID4, AnyUrl, BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from pymongo import IndexModel


PhoneNumber.phone_format = "E164"


class user_status_enum(str, Enum):
    inactive = "inactive"
    active = "active"
    blocked = "blocked"


class roles(str, Enum):
    owner = "owner"
    tenant = "tenant"
    family = "family"


class dwelling_list(BaseModel):
    community_id: Optional[UUID4] = None
    dwelling_id: Optional[UUID4] = None
    community_name: str
    block: Optional[str] = None
    floor_no: Optional[str] = None
    flat_no: Optional[str] = None
    role: Optional[roles] = roles.owner
    user_status: Optional[user_status_enum] = user_status_enum.inactive


class activity_info(BaseModel):
    updated_by: str
    updated_at: datetime


class meta_info(BaseModel):
    ver: Optional[float] = None
    created_by: Optional[str] = None
    created_at: Optional[datetime] = None
    activity: Optional[activity_info] = None


class app_users_model(Document):
    user_id: Optional[str]
    name: Optional[str] = None
    mobile: PhoneNumber
    email: Optional[EmailStr] = None
    profile_picture: Optional[AnyUrl] = None
    birth_date: Optional[date] = None
    dwelling: Optional[List[dwelling_list]] = []
    meta: meta_info

    class Settings:
        name = os.getenv("MOBILE_USERS_COLL")
        indexes = [
            "user_id",
            IndexModel([("mobile")]),
            IndexModel([("dwelling.dwelling_id")])
        ]
