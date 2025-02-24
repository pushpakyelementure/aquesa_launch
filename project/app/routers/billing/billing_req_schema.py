from pydantic import BaseModel
from typing import List, Optional
from datetime import date


class bill_create_req(BaseModel):
    year: int
    month: int
    fixed_cost: List[dict] = None
    variable_cost: Optional[List[dict]] = None


class bill_update_req(BaseModel):
    year: Optional[int] = None
    month: Optional[int] = None
    fixed_cost: Optional[List[dict]] = None
    variable_cost: Optional[List[dict]] = None
    bill_date: Optional[date] = None
