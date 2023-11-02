from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from db.models import get_db
from schemas import schemas
from logic import crud


admin_router = APIRouter(prefix='/admin', tags=['Admin'])


@admin_router.patch("/{user_id}/tokens/", response_model=schemas.User)
def change_tokens_value(user_id: int, tokens_value: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    user = db_user
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    user.tokens_value = tokens_value
    return crud.change_user_info(db, user)


@admin_router.post("/{user_id}/", response_model=schemas.User)
def make_admin(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    user = db_user
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_admin = True
    return crud.change_user_info(db, user)
