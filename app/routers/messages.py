# messages.py (router)
# basic messaging between sellers and recyclers
# keeping it simple REST for MVP, no websockets needed yet

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone

from app.database import get_db
from app.models.message import Message
from app.schemas.message import MessageCreate, MessageResponse

router = APIRouter(
    prefix="/api/v1/messages",
    tags=["messages"]
)

# send a message
@router.post("/", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def send_message(message: MessageCreate, db: Session = Depends(get_db)):
    # hardcoded sender_id until auth is merged in
    new_message = Message(
        sender_id=1,  # will be replaced with current user id from JWT
        recipient_id=message.recipient_id,
        offer_id=message.offer_id,
        message_text=message.message_text
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message

# get all messages for an offer
@router.get("/{offer_id}", response_model=List[MessageResponse])
def get_messages(offer_id: int, db: Session = Depends(get_db)):
    messages = db.query(Message).filter(Message.offer_id == offer_id).all()
    if not messages:
        raise HTTPException(status_code=404, detail="No messages found for this offer")
    return messages

# mark a message as read
@router.put("/{message_id}/read", response_model=MessageResponse)
def mark_as_read(message_id: int, db: Session = Depends(get_db)):
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    message.is_read = True
    message.read_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(message)
    return message