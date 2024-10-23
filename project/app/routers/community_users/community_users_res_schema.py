from datetime import date, datetime
from typing import List, Optional

from pydantic import UUID4, BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber

from app.db.models.community_user import comm_user_status, op_roles

PhoneNumber.phone_format = "E164"


class activity_info(BaseModel):
    updated_by: str
    updated_at: datetime


class meta_info(BaseModel):
    ver: float
    activity: activity_info


class create_res_model(BaseModel):
    community_id: UUID4
    user_id: str
    detail: str


class read_user(BaseModel):
    user_id: Optional[str] = None
    community_id: UUID4
    name: str
    mobile: PhoneNumber
    email: Optional[EmailStr] = None
    profile_picture: Optional[str] = None
    role: List[op_roles] = op_roles.admin
    birth_date: Optional[date] = None
    user_status: Optional[comm_user_status]


class update_comm_contact(BaseModel):
    community_id: UUID4
    user_id: str
    updated_details: dict
    detail: str
    meta: meta_info


class resp_comm_user(BaseModel):
    community_id: UUID4
    user_id: str
    updated_info: dict
    meta: meta_info
