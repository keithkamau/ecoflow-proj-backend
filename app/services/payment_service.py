from sqlalchemy.orm import Session
from datetime import datetime, timezone
import uuid
from app.models.payment import Payment, PaymentStatus, PaymentMethod
from app.models.transaction import Transaction, TransactionStatus


def get_payment_by_transaction(db: Session, transaction_id: int):
    return db.query(Payment).filter(Payment.transaction_id == transaction_id).first()


def get_all_payments(db: Session):
    return db.query(Payment).all()


def process_payment(db: Session, transaction_id: int, user_id: int, amount: float, payment_method: PaymentMethod):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        return None
    commission_amount = amount * 0.05
    mock_reference = f"MOCK-{uuid.uuid4().hex[:8].upper()}"
    payment = Payment(
        transaction_id=transaction_id,
        user_id=user_id,
        amount=amount,
        payment_method=payment_method,
        status=PaymentStatus.SUCCESS,
        reference=mock_reference,
        commission_rate=0.05,
        commission_amount=commission_amount
    )
    db.add(payment)
    transaction.status = TransactionStatus.COMPLETED
    transaction.completed_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(payment)
    return payment
