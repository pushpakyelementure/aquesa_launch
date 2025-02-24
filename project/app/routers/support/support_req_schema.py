from pydantic import BaseModel, AnyUrl
from typing import Optional, List
from datetime import datetime

from app.db.models.support import category_enum, status_enum


class timeline_dict(BaseModel):
    name: str
    date: datetime
    description: Optional[str] = None
    document: Optional[List[AnyUrl]] = None


class service_request(BaseModel):
    sr_id: str
    date: datetime
    category: Optional[category_enum]
    description: Optional[str] = None
    status: Optional[status_enum]
    documents: Optional[List[AnyUrl]] = None
    timeline: Optional[List[timeline_dict]] = None
