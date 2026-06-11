# transactions.py (router)
# transactions are created when an offer is accepted
# and move through a status pipeline until payment is complete

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone

from app.database import get_db
from app.models.transaction import Transaction, TransactionStatus
from app.models.offer import Offer, OfferStatus
from app.schemas.transaction import TransactionCreate, TransactionUpdate, TransactionResponse

router = APIRouter(
    prefix="/api/v1/transactions",
    tags=["transactions"]
)

# create a transaction — this happens when a seller accepts an offer
@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    # make sure the offer exists and is accepted
    offer = db.query(Offer).filter(Offer.id == transaction.offer_id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    if offer.status != OfferStatus.ACCEPTED:
        raise HTTPException(status_code=400, detail="Can only create a transaction from an accepted offer")

    # check if a transaction already exists for this offer
    existing = db.query(Transaction).filter(Transaction.offer_id == transaction.offer_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="A transaction already exists for this offer")

    new_transaction = Transaction(**transaction.model_dump())
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction

# get all transactions
@router.get("/", response_model=List[TransactionResponse])
def get_transactions(seller_id: int = None, recycler_id: int = None, db: Session = Depends(get_db)):
    query = db.query(Transaction)
    if seller_id:
        query = query.filter(Transaction.seller_id == seller_id)
    if recycler_id:
        query = query.filter(Transaction.recycler_id == recycler_id)
    return query.all()

# get a single transaction
@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

# update transaction status as it moves through the pipeline
@router.put("/{transaction_id}", response_model=TransactionResponse)
def update_transaction(transaction_id: int, update: TransactionUpdate, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    # mark completed_at when the transaction finishes
    if update.status == TransactionStatus.COMPLETED:
        transaction.completed_at = datetime.now(timezone.utc)

    transaction.status = update.status
    db.commit()
    db.refresh(transaction)
    return transaction