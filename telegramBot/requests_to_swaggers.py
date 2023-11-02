from fastapi import FastAPI
from endpoints.metadata import tags_metadata
from schemas.schemas import *


app = FastAPI(openapi_tags=tags_metadata)

@app.post('/users/')
async def create_user(tg_id: int, username: str, tokens_value: int, user: User=User):
    return {'tg_id' : tg_id, 'username' : username, 'tokens_value' : tokens_value, **user.dict()}

@app.post('/photos/{user_id}/')
async def create_photo_for_user(id: int, owner_id: int, url: str, is_detection_correct: bool, is_favorite: bool, photo: Photo=Photo):
    return {'id' : id, 'owner_id' : owner_id, 'url' : url, 'is_detection_correct' : is_detection_correct, 'is_favorite' : is_favorite, **photo.dict()}

