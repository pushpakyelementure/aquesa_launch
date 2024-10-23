from pydantic import BaseModel
from pydantic import UUID4, AnyUrl
from datetime import date
from typing import Optional

from app.db.models.subscription import subscription_enum


class subscription_res(BaseModel):
    detail: str


class get_all_invoices(BaseModel):
    community_id: UUID4
    subscription_invoice_id: UUID4
    month: date
    subscription_plan: subscription_enum
    billing_amount: float
    invoice_date: date
    payment_due_date: date
    invoice_url: Optional[AnyUrl]


class download_invoices(BaseModel):
    invoice_url: AnyUrl
