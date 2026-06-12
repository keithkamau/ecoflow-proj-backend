# offer.py (schema)
# these define what data comes in and goes out of the offer endpoints
# Pydantic handles the validation automatically

from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime
from typing import Optional
from app.models.offer import OfferStatus

# what we expect when someone creates an offer
class OfferCreate(BaseModel):
    listing_id: int
    offered_price: float
    quantity: float
    note: Optional[str] = None

    # make sure the price and quantity are positive
    @field_validator("offered_price", "quantity")
    def must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("must be greater than zero")
        return v

# what we expect when someone updates an offer
class OfferUpdate(BaseModel):
    status: OfferStatus
    note: Optional[str] = None

# what we send back when returning offer data
class OfferResponse(BaseModel):
    id: int
    listing_id: int
    recycler_id: int
    offered_price: float
    quantity: float
    status: OfferStatus
    note: Optional[str]
    created_at: datetime
    expires_at: datetime

    model_config = ConfigDict(from_attributes=True)