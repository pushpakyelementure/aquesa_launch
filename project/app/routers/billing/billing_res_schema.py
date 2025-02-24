from pydantic import BaseModel, UUID4
from typing import Optional, List
from datetime import date, datetime


class bill_create_res(BaseModel):
    detail: str


class dwell_bill(BaseModel):
    dwelling_id: UUID4
    bill_id: UUID4
    year: int
    month: int
    block: str
    flat_no: str
    consumption: int
    fixed_cost: float
    variable_cost: float
    total_cost: float


class bill_setup_comm_res(BaseModel):
    community_id: UUID4
    year: int
    month: int
    Total_csm: Optional[int] = None
    fixed_cost: Optional[List[dict]] = None
    variable_cost: Optional[List[dict]] = None
    total_fixed_cost: float
    total_variable_cost: float
    bill_date: date
    dwelling_bill: Optional[List[dwell_bill]] = None


class activity_info(BaseModel):
    updated_by: str
    updated_at: datetime


class meta_info(BaseModel):
    ver: float
    activity: activity_info


class update_bill_info(BaseModel):
    detail: str
    updated_info: dict
    meta: meta_info
