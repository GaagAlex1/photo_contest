from fastapi import APIRouter, Body
from auth.router import user_dependency
from database import db_dependency
from models.schemas import *
from models.orm import *

vote_router = APIRouter(prefix='/vote')

@vote_router.post('/add/')
async def add_photo(
        user: user_dependency,
        db: db_dependency,
        photo_id: int = Body(...),
        rate: int = Body(...)
) -> VoteBase:
    vote: Vote = Vote(
        author_id=user.id,
        photo_id=photo_id,
        rate=rate
    )

    db.add(vote)
    await db.commit()

    return VoteBase.from_orm(vote)

@vote_router.get('/get_all/')
async def get_all(
        db: db_dependency,
        photo_id: int
) -> List[VoteBase]:
    photo: Photo = await db.get(Photo, photo_id)
    return [VoteBase.from_orm(vote) for vote in photo.votes]


@vote_router.get('/get/')
async def get_one(
        db: db_dependency,
        vote_id: int
) -> PhotoBase:
    vote: Vote = await db.get(Comment, vote_id)
    return VoteBase.from_orm(vote)