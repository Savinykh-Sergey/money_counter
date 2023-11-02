from fastapi import APIRouter, Depends, UploadFile, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
import datetime

from db.models import get_db
from schemas import schemas
from logic import crud
from neuro_processing.photo_processor import detect_objects_on_image, draw_rectangles


photos_router = APIRouter(prefix='/photos', tags=['Photos'])


@photos_router.post("/{user_id}/", response_class=FileResponse)
async def create_photo_for_user(
    user_id: int, file: UploadFile, db: Session = Depends(get_db)
):
    if not file.content_type.__contains__('image'):
        raise HTTPException(status_code=404, detail="Filetype is incorrect")
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    file_name = f"{current_time}_{file.filename}"
    file_path = f"photos/unprocessed/{file_name}"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    photo = schemas.PhotoCreate(name=file_name, url=file_path, is_favorite=False)
    result_photo = crud.create_user_photo(db=db, photo=photo, user_id=user_id)
    сoords_list = detect_objects_on_image(file_path)
    if len(сoords_list) < 1:
        return file_path
    return draw_rectangles(file_name, сoords_list)


@photos_router.get("/{user_id}/", response_model=list[schemas.Photo])
def read_photos(user_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    photos = crud.get_photos(db, user_id, skip=skip, limit=limit)
    return photos


@photos_router.get("/{user_id}/favorite", response_model=list[schemas.Photo])
def read_photos(user_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    fav_photos = crud.get_favorite_photos(db, user_id, skip=skip, limit=limit)
    return fav_photos

