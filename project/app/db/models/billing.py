from pydantic import BaseModel, UUID4, AnyUrl
from beanie import Document
from typing import Optional
from datetime import date
from typing import List
from enum import Enum
import os


class month_enum(str, Enum):
    jan = "jan"
    feb = "feb"
    march = "march"
    april = "april"
    may = "may"
    june = "june"
    july = "july"
    august = "august"
    sep = "sep"
    oct = "oct"
    nov = "nov"
    dec = "dec"


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
    bill_url: Optional[AnyUrl] = None


class billing_model(Document):
    community_id: UUID4
    year: int
    month: int
    fixed_cost: List[dict]
    total_fixed_cost: Optional[float]
    variable_cost: List[dict]
    total_variable_cost: Optional[float]
    bill_date: date
    dwelling_bill: Optional[List[dwell_bill]] = None

    class Settings:
        name = os.getenv("BILLING_COLL")
        indexes = [
            "community_id",
            "dwelling_bill.bill_id",
        ]
