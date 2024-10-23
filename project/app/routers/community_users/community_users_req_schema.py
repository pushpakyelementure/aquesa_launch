from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber

from app.db.models.community_user import comm_user_status, op_roles, title_enum

PhoneNumber.phone_format = "E164"


class user_create(BaseModel):
    name: str
    mobile: PhoneNumber
    title: title_enum
    email: Optional[EmailStr] = None
    password: str
    birth_date: Optional[date] = None
    role: op_roles
    user_status: Optional[comm_user_status]


class update_comm_contact(BaseModel):
    mobile: Optional[PhoneNumber] = None
    email: Optional[EmailStr] = None
    name: Optional[str] = None


class update_comm_user(BaseModel):
    name: Optional[str] = None
    mobile: Optional[PhoneNumber] = None
    title: Optional[title_enum] = title_enum.manager
    email: Optional[EmailStr] = None
    birth_date: Optional[date] = None
    role: op_roles
    user_status: Optional[comm_user_status] = None
