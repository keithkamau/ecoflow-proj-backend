# offers.py (router)
# handles all the offer-related endpoints
# recyclers create offers, sellers accept or reject them

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone

from app.database import get_db
from app.models.offer import Offer, OfferStatus
from app.schemas.offer import OfferCreate, OfferUpdate, OfferResponse

router = APIRouter(
    prefix="/api/v1/offers",
    tags=["offers"]
)

# create a new offer on a listing
@router.post("/", response_model=OfferResponse, status_code=status.HTTP_201_CREATED)
def create_offer(offer: OfferCreate, db: Session = Depends(get_db)):
    # for now we're using a hardcoded recycler_id until auth is merged in
    new_offer = Offer(
        listing_id=offer.listing_id,
        recycler_id=1,  # will be replaced with current user id from JWT
        offered_price=offer.offered_price,
        quantity=offer.quantity,
        note=offer.note
    )
    db.add(new_offer)
    db.commit()
    db.refresh(new_offer)
    return new_offer

# get all offers — can filter by listing or recycler
@router.get("/", response_model=List[OfferResponse])
def get_offers(listing_id: int = None, recycler_id: int = None, db: Session = Depends(get_db)):
    query = db.query(Offer)
    if listing_id:
        query = query.filter(Offer.listing_id == listing_id)
    if recycler_id:
        query = query.filter(Offer.recycler_id == recycler_id)
    return query.all()

# get a single offer by id
@router.get("/{offer_id}", response_model=OfferResponse)
def get_offer(offer_id: int, db: Session = Depends(get_db)):
    offer = db.query(Offer).filter(Offer.id == offer_id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    return offer

# accept, reject or counter an offer
@router.put("/{offer_id}", response_model=OfferResponse)
def update_offer(offer_id: int, update: OfferUpdate, db: Session = Depends(get_db)):
    offer = db.query(Offer).filter(Offer.id == offer_id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")

    # can't update an offer that's already been closed
    if offer.status in [OfferStatus.ACCEPTED, OfferStatus.REJECTED, OfferStatus.EXPIRED]:
        raise HTTPException(status_code=400, detail="This offer is already closed")

    offer.status = update.status
    if update.note:
        offer.note = update.note

    db.commit()
    db.refresh(offer)
    return offer

# delete an offer — only if it's still pending
@router.delete("/{offer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_offer(offer_id: int, db: Session = Depends(get_db)):
    offer = db.query(Offer).filter(Offer.id == offer_id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    if offer.status != OfferStatus.PENDING:
        raise HTTPException(status_code=400, detail="Can only delete pending offers")
    db.delete(offer)
    db.commit()