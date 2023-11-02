from sqlalchemy.orm import Session

from db import models
from schemas import schemas


photos_directory = "./photos/"


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_messages(db: Session, user_id: int):
    return db.query(models.Messages).filter(models.User.id == user_id).all()


def create_user_message(db: Session, msg: schemas.MessageCreate):
    db_message = models.Message(**msg.dict())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def change_user_info(db: Session, user: schemas.User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_photos(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Photo).filter(models.Photo.owner_id == user_id).limit(100).all()


def get_favorite_photos(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Photo).filter(models.Photo.owner_id == user_id).filter(models.Photo.is_favorite).limit(100).all()


def create_user_photo(db: Session, photo: schemas.PhotoCreate, user_id: int):
    db_item = models.Photo(**photo.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
