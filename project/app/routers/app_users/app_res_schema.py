from datetime import date, datetime
from typing import List, Optional

from pydantic import UUID4, AnyUrl, BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber

from app.db.models.app_user import roles, user_status_enum

PhoneNumber.phone_format = "E164"


class user_create_resp_model(BaseModel):
    user_id: str
    detail: str


class activity_info(BaseModel):
    updated_by: str
    updated_at: datetime


class update_meta_info(BaseModel):
    ver: float
    activity: activity_info


class meta_info(BaseModel):
    ver: float
    created_by: Optional[str] = None
    created_at: Optional[datetime] = None
    activity: Optional[activity_info]


class dwell_info(BaseModel):
    community_id: Optional[UUID4] = None
    community_name: str
    dwelling_id: Optional[UUID4] = None
    block: str
    floor_no: str
    flat_no: str
    role: Optional[roles] = roles.owner
    user_status: Optional[user_status_enum] = user_status_enum.inactive


class user_read_resp_model(BaseModel):
    user_id: str
    name: str
    mobile: PhoneNumber
    email: EmailStr
    birth_date: Optional[date] = None
    profile_picture: Optional[AnyUrl] = None
    dwelling: List[dwell_info]
    meta: meta_info


class user_update_resp_model(BaseModel):
    user_id: Optional[str] = None
    detail: Optional[str] = None
    updated_info: Optional[dict] = None
    meta: Optional[update_meta_info] = None


class user_patch_resp_model(BaseModel):
    user_id: Optional[str] = None
    detail: Optional[str] = None
    # meta: Optional[update_meta_info] = None
