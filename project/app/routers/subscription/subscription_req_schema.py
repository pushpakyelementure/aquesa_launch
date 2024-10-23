from pydantic import BaseModel
from datetime import date

from app.db.models.subscription import subscription_enum


class create_subscription(BaseModel):
    month: date
    subscription_plan: subscription_enum
    billing_amount: float
    invoice_date: date
    payment_due_date: date


class update_subscription(BaseModel):
    month: date
    subscription_plan: subscription_enum
    billing_amount: float
    invoice_date: date
    payment_due_date: date
