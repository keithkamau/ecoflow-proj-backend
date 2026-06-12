from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.payment import PaymentCreate, PaymentResponse
from app.services.payment_service import process_payment, get_payment_by_transaction, get_all_payments

router = APIRouter(prefix="/api/v1/payments", tags=["payments"])


@router.post("/", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    result = process_payment(
        db,
        transaction_id=payment.transaction_id,
        user_id=payment.user_id,
        amount=payment.amount,
        payment_method=payment.payment_method,
    )
    if result is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return result


@router.get("/{transaction_id}", response_model=PaymentResponse)
def get_payment(transaction_id: int, db: Session = Depends(get_db)):
    payment = get_payment_by_transaction(db, transaction_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


@router.get("/", response_model=List[PaymentResponse])
def list_payments(db: Session = Depends(get_db)):
    return get_all_payments(db)
