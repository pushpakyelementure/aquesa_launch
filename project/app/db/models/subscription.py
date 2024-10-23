from beanie import Document
from pydantic import UUID4, AnyUrl
from typing import Optional
from datetime import date
from enum import Enum
import os


class subscription_enum(str, Enum):
    active = "active"
    inactive = "inactive"


class subscription(Document):
    community_id: UUID4
    subscription_invoice_id: UUID4
    month: date
    subscription_plan: subscription_enum = subscription_enum.active
    billing_amount: float
    invoice_date: date
    payment_due_date: date
    invoice_url: Optional[AnyUrl] = None

    class Settings:
        name = os.getenv("SUBSCRIPTION_COLL")
        indexes = [
            "community_id",
            "subscription_invoice_id"
        ]
