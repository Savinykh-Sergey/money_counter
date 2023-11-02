from typing import Optional, Any
from pydantic import BaseModel, Json


class History(BaseModel):
    owner_id: int
    sum: float = 0
    messages: list[str]


class MessageCreate(BaseModel):
    owner_id: int
    message_text: str
    message_sum: float


class Message(MessageCreate):
    id: int

    class Config:
        orm_mode = True


class PhotoBase(BaseModel):
    name: str
    url: str
    is_favorite: bool


class PhotoCreate(PhotoBase):
    pass


class Photo(BaseModel):
    id: int
    owner_id: int
    name: str
    url: str
    is_detection_correct: Optional[bool]
    is_favorite: bool

    class Config:
        orm_mode = True


class DetectedPhoto(BaseModel):
    id: int
    owner_id: int
    name: str
    url: str
    is_detection_correct: Optional[bool]
    is_favorite: bool

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    tg_id: int
    first_name: str
    last_name: str
    username: str
    hash: str
    tokens_value: int = 10


class UserCreate(UserBase):
    pass


class User(BaseModel):
    id: int
    tg_id: int
    first_name: str
    last_name: str
    username: str
    hash: str
    tokens_value: int = 10
    is_admin: Optional[bool]
    sum: float = 0
    photos: Optional[list[Photo]] = []
    detected_photos: Optional[list[Photo]] = []
    messages: list[Message]

    class Config:
        orm_mode = True
