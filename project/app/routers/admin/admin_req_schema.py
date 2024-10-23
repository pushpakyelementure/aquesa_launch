from typing import Optional

from pydantic import BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber

from app.db.models.admin_user import user_roles, user_status

PhoneNumber.phone_format = "E164"


class admin_user_create(BaseModel):
    name: str
    employee_id: Optional[str] = None
    mobile: PhoneNumber
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    user_status: user_status
    role: user_roles


class update_admin_user(BaseModel):
    name: Optional[str] = None
    mobile: Optional[PhoneNumber] = None
    email: Optional[EmailStr] = None
    role: Optional[user_roles] = user_roles.admin


class update_admin_user_role(BaseModel):
    role: Optional[user_roles] = user_roles.admin
