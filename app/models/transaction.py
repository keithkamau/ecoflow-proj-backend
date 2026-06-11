# transaction.py
# A transaction is created when a seller accepts an offer
# it tracks the full lifecycle from acceptance to payment

from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Enum
from datetime import datetime, timezone
import enum

from app.database import Base

# all the stages a transaction goes through
class TransactionStatus(enum.Enum):
    OFFER_ACCEPTED = "offer_accepted"         # seller just accepted the offer
    PICKUP_SCHEDULED = "pickup_scheduled"     # recycler has set a pickup time
    PICKUP_COMPLETED = "pickup_completed"     # materials have been collected
    PAYMENT_PENDING = "payment_pending"       # waiting for payment to go through
    COMPLETED = "completed"                   # everything done, payment sent
    DISPUTED = "disputed"                     # something went wrong, under review
    CANCELLED = "cancelled"                   # called off before completion

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    # the listing and offer this transaction came from
    listing_id = Column(Integer, nullable=False)
    offer_id = Column(Integer, ForeignKey("offers.id"), nullable=False)

    # who's involved
    seller_id = Column(Integer, nullable=False)
    recycler_id = Column(Integer, nullable=False)

    # the agreed terms when the offer was accepted
    agreed_price = Column(Float, nullable=False)
    final_quantity = Column(Float, nullable=False)

    # total = agreed_price * final_quantity
    final_price = Column(Float, nullable=False)

    # where we are in the process
    status = Column(Enum(TransactionStatus), default=TransactionStatus.OFFER_ACCEPTED)

    # timestamps so we can track how long each stage takes
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    completed_at = Column(DateTime, nullable=True)

    # relationships — commented out until all models exist
    # offer = relationship("Offer", back_populates="transaction")
    # seller = relationship("User", foreign_keys=[seller_id])
    # recycler = relationship("User", foreign_keys=[recycler_id])
    # payment = relationship("Payment", back_populates="transaction")
    # pickup = relationship("Pickup", back_populates="transaction")