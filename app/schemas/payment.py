# payment.py (schema)
# defines payment request and response shapes

from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional
from app.models.payment import PaymentMethod, PaymentStatus

# what we need to process a payment
class PaymentCreate(BaseModel):
    transaction_id: int
    user_id: int
    amount: float
    payment_method: PaymentMethod = PaymentMethod.MPESA

    @field_validator("amount")
    def amount_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("payment amount must be greater than zero")
        return v

# what we send back after processing a payment
class PaymentResponse(BaseModel):
    id: int
    transaction_id: int
    user_id: int
    amount: float
    payment_method: PaymentMethod
    status: PaymentStatus
    reference: Optional[str]
    commission_rate: float
    commission_amount: Optional[float]
    created_at: datetime

    class Config:
        from_attributes = True