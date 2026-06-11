# payments.py (router)
# handles payment processing
# using a mock M-Pesa for MVP — swap with real Daraja API later

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid

from app.database import get_db
from app.models.payment import Payment, PaymentStatus
from app.models.transaction import Transaction, TransactionStatus
from app.schemas.payment import PaymentCreate, PaymentResponse

router = APIRouter(
    prefix="/api/v1/payments",
    tags=["payments"]
)

# process a payment for a transaction
@router.post("/", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    # make sure the transaction exists
    transaction = db.query(Transaction).filter(Transaction.id == payment.transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    # calculate the platform commission
    commission_amount = payment.amount * 0.05  # 5% commission

    # generate a mock payment reference — replace with real M-Pesa reference later
    mock_reference = f"MOCK-{uuid.uuid4().hex[:8].upper()}"

    new_payment = Payment(
        transaction_id=payment.transaction_id,
        user_id=payment.user_id,
        amount=payment.amount,
        payment_method=payment.payment_method,
        status=PaymentStatus.SUCCESS,  # mock always succeeds for now
        reference=mock_reference,
        commission_rate=0.05,
        commission_amount=commission_amount
    )

    db.add(new_payment)

    # update the transaction status to completed
    transaction.status = TransactionStatus.COMPLETED
    db.commit()
    db.refresh(new_payment)
    return new_payment

# get payment status for a transaction
@router.get("/{transaction_id}", response_model=PaymentResponse)
def get_payment(transaction_id: int, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.transaction_id == transaction_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

# get all payments
@router.get("/", response_model=List[PaymentResponse])
def get_payments(db: Session = Depends(get_db)):
    return db.query(Payment).all()