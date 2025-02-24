from pydantic import BaseModel, UUID4
from typing import List, Optional

from app.db.models.aqs_enums import aggregation_enum


# class csm_aggregation_by_community(BaseModel):
#     year: int
#     month: int
#     date: Optional[int] = None
#     aggregation: aggregation_enum
#     consumption: List[int]


class consumption_by_community(BaseModel):
    total_consumption: int
    # data: List[csm_aggregation_by_community]


class DwellingConsumption(BaseModel):
    dwelling_id: UUID4
    total_consumption: int


class TopDwellingsConsumption(BaseModel):
    aggregation: str
    community_id: UUID4
    top_5_dwellings: List[DwellingConsumption]


# class data(BaseModel):
#     year: str
#     month: str
#     date: str
#     aggregation: aggregation_enum
#     consumption: int  # Ensure this field is included


# class DwellingsConsumption(BaseModel):
#     total_consumption: int
#     community_id: UUID4
#     dwelling_id: UUID4
#     consumption_data: List[data]
