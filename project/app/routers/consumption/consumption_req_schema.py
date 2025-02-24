from pydantic import BaseModel, UUID4
from datetime import date
from typing import Optional

from app.db.models.aqs_enums import aggregation_enum


class top_5_consumption(BaseModel):
    # community_id: UUID4
    start_date: date
    end_date: Optional[date] = None
    aggregation: aggregation_enum


class day_consumption(BaseModel):
    community_id: UUID4
    start_date: date
    end_date: Optional[date] = None
    aggregation: aggregation_enum
