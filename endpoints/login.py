from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from db.models import get_db
from schemas import schemas
from logic import crud


login_router = APIRouter(prefix='/login', tags=['Login'])


@login_router.post("/")
def log_in(user: schemas.User, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    response = JSONResponse(content={"message": "куки установлены"})
    if db_user is None:
        user = crud.create_user(user, db)
    else:
        user = db_user

    response.set_cookie(key="user_id", value=user.id)
    return response
