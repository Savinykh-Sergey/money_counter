from typing import List, Optional

from sqlalchemy import Column, Integer, String, Boolean, Float, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./db/sql_app.db"
engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(autoflush=False, bind=engine)
Base = declarative_base()
Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    tg_id = Column(Integer, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    username = Column(String, nullable=False)
    hash = Column(String, nullable=False)
    tokens_value = Column(Integer, default=10, nullable=False)
    is_admin = Column(String)
    sum = Column(Float, default=0)

    photos = relationship("Photo", back_populates="owner")
    detected_photos = relationship("DetectedPhoto", back_populates="owner")
    messages = relationship("Message", back_populates="owner")


class Photo(Base):
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    url = Column(String, unique=True, nullable=False)
    is_detection_correct = Column(Boolean)
    is_favorite = Column(Boolean)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="photos")


class DetectedPhoto(Base):
    __tablename__ = "detected_photos"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    url = Column(String, unique=True, nullable=False)
    is_detection_correct = Column(Boolean)
    is_favorite = Column(Boolean)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="detected_photos")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    message_text = Column(String, default="", nullable=False)
    message_sum = Column(Float, default=0, nullable=False)

    owner = relationship("User", back_populates="messages")
