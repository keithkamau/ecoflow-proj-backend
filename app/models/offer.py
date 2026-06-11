# offer.py
# This model represents an offer a recycler makes on a seller's listing
# when a recycler sees a listing they like, they create an offer with their price

from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Enum
from datetime import datetime, timedelta, timezone
import enum

from app.database import Base

# the possible states an offer can be in
class OfferStatus(enum.Enum):
    PENDING = "pending"       # just created, waiting for seller response
    ACCEPTED = "accepted"     # seller said yes
    REJECTED = "rejected"     # seller said no
    COUNTERED = "countered"   # seller came back with a different price
    EXPIRED = "expired"       # nobody responded in time

class Offer(Base):
    __tablename__ = "offers"

    id = Column(Integer, primary_key=True, index=True)
    # will be a ForeignKey to listings.id once that model is merged in
    listing_id = Column(Integer, nullable=False)

    # will be a ForeignKey to users.id once that model is merged in
    recycler_id = Column(Integer, nullable=False)

    # how much they're offering per kg and how much they want
    offered_price = Column(Float, nullable=False)
    quantity = Column(Float, nullable=False)

    # current state of the offer
    status = Column(Enum(OfferStatus), default=OfferStatus.PENDING, nullable=False)

    # offers expire after 24 hours if no response
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    expires_at = Column(DateTime, default=lambda: datetime.now(timezone.utc) + timedelta(hours=24))

    # optional note the recycler can add with their offer
    note = Column(String, nullable=True)

    # relationships we'll use to access related data easily
    # these will work once the other models are in place
    # listing = relationship("Listing", back_populates="offers")
    # recycler = relationship("User", back_populates="offers")
    # transaction = relationship("Transaction", back_populates="offer") 