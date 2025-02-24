from pydantic import UUID4,BaseModel
from datetime import datetime
from typing import Optional

from app.db.models.alert import leakege


class create_alert(BaseModel):
    device_id: UUID4
    timestamp: datetime
    alert: Optional[leakege] = leakege.no_leakage
