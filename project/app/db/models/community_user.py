import os
from datetime import datetime
from enum import Enum
from typing import List, Optional

from beanie import Document
from pydantic import UUID4, BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber

PhoneNumber.phone_format = "E164"


class title_enum(str, Enum):
    treasurer = "treasurer"
    manager = "manager"
    secretary = "secretary"
    superuser = "superuser"
    admin = "admin"
    support = "support"


class op_roles(str, Enum):
    admin = "admin"
    superuser = "superuser"
    manager = "manager"


class comm_user_status(str, Enum):
    active = "active"
    inactive = "inactive"
    deleted = "deleted"


class activity_info(BaseModel):
    updated_by: Optional[str] = None
    updated_at: Optional[datetime] = None


class meta_data(BaseModel):
    ver: float
    created_by: Optional[str] = None
    created_at: Optional[datetime] = None
    activity: Optional[activity_info] = None


class community_users_model(Document):
    user_id: Optional[str]
    community_id: UUID4
    name: str
    title: title_enum = title_enum.manager
    mobile: PhoneNumber
    email: Optional[EmailStr]
    password: Optional[str] = None
    profile_picture: Optional[str] = None
    role: List[op_roles] = [op_roles.admin]
    birth_date: Optional[datetime]
    user_status: Optional[comm_user_status]
    meta: meta_data

    class Settings:
        name = os.getenv("COMMUNITY_USERS_COLL")
        indexes = [
            "user_id",
            "mobile",
            "email"
            "community_id"
        ]
