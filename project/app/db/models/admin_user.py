import os
from datetime import datetime
from enum import Enum
from typing import List, Optional

from beanie import Document
from pydantic import BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber

PhoneNumber.phone_format = "E164"


class user_roles(str, Enum):
    admin = "admin"
    superuser = "superuser"
    support = "support"
    field = "field"


class user_status(str, Enum):
    active = "active"
    inactive = "inactive"
    deleted = "deleted"


class activity_info(BaseModel):
    updated_by: Optional[str] = None
    updated_at: Optional[datetime] = None


class meta_data(BaseModel):
    created_by: Optional[str] = None
    created_at: Optional[datetime] = None
    activity: Optional[activity_info] = None


class admin_user_model(Document):
    user_id: Optional[str]
    employee_id: str
    name: str
    mobile: PhoneNumber
    email: Optional[EmailStr]
    password: Optional[str] = None
    role: List[user_roles] = [user_roles.admin]
    user_status: user_status
    meta: meta_data

    class Settings:
        name = os.getenv("ADMIN_USERS_COLL")
        indexes = [
            "user_id",
            "mobile",
            "email",
        ]
