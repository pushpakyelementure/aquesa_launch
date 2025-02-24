from pydantic import BaseModel, UUID4
from typing import List, Dict
from datetime import datetime


class dwell_users(BaseModel):
    owners: int
    tenants: int


class get_info_of_community(BaseModel):
    community_id: UUID4
    Total_Flats: int
    Total_Devices: int
    Residence_Distribution: dwell_users


class block_csm(BaseModel):
    block: str
    # date: datetime
    total_monthly_consumption: int


class get_tower_consumption(BaseModel):
    community_id: UUID4
    blocks: List[block_csm]


class BlockConsumption(BaseModel):
    blockwise_consumption: Dict[str, float]


class water_usage_Consumption(BaseModel):
    total_consumption: int
    average_consumption: int
    total_limit: int
    excess_consumption: int
    status: str
    