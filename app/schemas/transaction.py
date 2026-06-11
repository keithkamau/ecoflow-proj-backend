# transaction.py (schema)
# defines the shape of transaction data coming in and going out

from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.transaction import TransactionStatus

# transactions are created automatically when an offer is accepted
# so we only need the offer_id to create one
class TransactionCreate(BaseModel):
    offer_id: int
    listing_id: int
    seller_id: int
    recycler_id: int
    agreed_price: float
    final_quantity: float
    final_price: float

# for updating the transaction status as it moves through the pipeline
class TransactionUpdate(BaseModel):
    status: TransactionStatus

# what we send back when returning transaction data
class TransactionResponse(BaseModel):
    id: int
    listing_id: int
    offer_id: int
    seller_id: int
    recycler_id: int
    agreed_price: float
    final_quantity: float
    final_price: float
    status: TransactionStatus
    created_at: datetime
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True