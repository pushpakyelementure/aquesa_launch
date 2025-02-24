from pydantic import BaseModel, UUID4, AnyUrl
from typing import Optional, List
from datetime import datetime


from app.db.models.support import category_enum, status_enum


class create_ticket(BaseModel):
    detail: str


class timeline_dict(BaseModel):
    name: str
    date: datetime
    description: Optional[str] = None
    document: Optional[List[AnyUrl]] = None


class meta_info(BaseModel):
    created_at: datetime
    created_by: str


class get_tickets(BaseModel):
    sr_id: str
    community_id: UUID4
    dwelling_id: UUID4
    date: datetime
    category: Optional[category_enum]
    description: Optional[str] = None
    status: Optional[status_enum]
    documents: Optional[List[AnyUrl]]
    timeline: Optional[List[timeline_dict]]
    meta: meta_info


class get_sr_id(BaseModel):
    sr_id: str
    community_id: UUID4
    dwelling_id: UUID4
    date: datetime
    category: Optional[category_enum]
    description: Optional[str] = None
    status: Optional[status_enum]
    documents: Optional[List[AnyUrl]]
    timeline: Optional[List[timeline_dict]]
    meta: meta_info
