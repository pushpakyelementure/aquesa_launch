from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber

from app.db.models.admin_user import user_roles


class activity_info(BaseModel):
    updated_by: str
    updated_at: datetime


class meta_info(BaseModel):
    activity: activity_info


class create_res_model(BaseModel):
    user_id: str
    detail: str


class read_admin_user(BaseModel):
    user_id: Optional[str] = None
    employee_id: Optional[str] = None
    name: str
    mobile: PhoneNumber
    email: Optional[EmailStr] = None
    role: List[user_roles] = user_roles.admin


class resp_update_comm_user(BaseModel):
    user_id: str
    updated_info: dict
    meta: meta_info


class user_role_change(BaseModel):
    user_id: str
    detail: str
