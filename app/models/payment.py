# payment.py
# Tracks payments made at the end of a transaction
# for MVP we're mocking M-Pesa but the model is ready for the real thing

from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Enum
from datetime import datetime, timezone
import enum

from app.database import Base

class PaymentMethod(enum.Enum):
    MPESA = "mpesa"       # primary payment method for Kenya
    CARD = "card"         # fallback option
    BANK = "bank"         # for larger recycler payouts

class PaymentStatus(enum.Enum):
    PENDING = "pending"       # payment initiated but not confirmed
    SUCCESS = "success"       # money sent successfully
    FAILED = "failed"         # something went wrong
    REFUNDED = "refunded"     # payment was reversed

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)

    # which transaction this payment is for
    transaction_id = Column(Integer, ForeignKey("transactions.id"), nullable=False)

    # who is receiving the payment (the seller)
    user_id = Column(Integer, nullable=False)

    # payment details
    amount = Column(Float, nullable=False)
    payment_method = Column(Enum(PaymentMethod), default=PaymentMethod.MPESA)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)

    # reference number from M-Pesa or card processor
    # we'll store the mock reference for now
    reference = Column(String, nullable=True)

    # platform takes a small commission on each transaction
    commission_rate = Column(Float, default=0.05)  # 5% default
    commission_amount = Column(Float, nullable=True)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # relationships — commented out until all models exist
    # transaction = relationship("Transaction", back_populates="payment")
    # user = relationship("User", back_populates="payments")