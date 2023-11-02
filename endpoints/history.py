from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.models import get_db
from schemas import schemas
from logic import crud


history_router = APIRouter(prefix='/history', tags=['History'])


@history_router.get("/{user_id}/", response_model=list[schemas.Message])
def get_user_history(user_id: int, db: Session = Depends(get_db)):
    messages = crud.get_user_messages(db, user_id)
    if messages is None:
        raise HTTPException(status_code=404, detail="User not found")
    return messages


@history_router.post("/{user_id}/", response_model=schemas.Message)
def create_user_message(user_id: int, db: Session = Depends(get_db)):
    # sum, text = get_photo_info()
    # msg = schemas.MessageCreate(owner_id=user_id, message_sum=sum, message_text=text)
    # return crud.create_user_message(msg)
    pass
