from fastapi import APIRouter, Depends, Body, File, UploadFile
import uuid
from auth.router import user_dependency
from database import db_dependency
from models.schemas import *
from models.orm import *
import os

photo_router = APIRouter(prefix='/photo')

@photo_router.post('/add/')
async def add_photo(
        user: user_dependency,
        db: db_dependency,
        contest_id: int = Body(...),
        photo: UploadFile = File(...)
) -> PhotoBase:
    photo_path: str = 'photos'
    os.makedirs(photo_path, exist_ok=True)

    file_extension: str = os.path.splitext(photo.filename)[1]
    filename: str = str(uuid.uuid4()) + file_extension
    file_location = os.path.join(photo_path, filename)

    with open(file_location, 'wb') as file:
        photo_content = await photo.read()
        file.write(photo_content)

    photo: Photo = Photo(
        author_id=user.id,
        contest_id=contest_id,
        url=file_location,
    )

    db.add(photo)
    await db.commit()

    return PhotoBase.from_orm(photo)

@photo_router.get('/get_all/')
async def get_all(
        db: db_dependency,
        contest_id: int
) -> List[PhotoBase]:
    contest: Contest = await db.get(Contest, contest_id)
    return [PhotoBase.from_orm(photo) for photo in contest.photos]


@photo_router.get('/get/')
async def get_one(
        db: db_dependency,
        photo_id: int
) -> PhotoBase:
    photo: Photo = await db.get(Photo, photo_id)
    return PhotoBase.from_orm(photo)
