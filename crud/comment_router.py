from fastapi import APIRouter, Body
from auth.router import user_dependency
from database import db_dependency
from models.schemas import *
from models.orm import *

comment_router = APIRouter(prefix='/comment')

@comment_router.post('/add/')
async def add_photo(
        user: user_dependency,
        db: db_dependency,
        photo_id: int = Body(...),
        text: str = Body(...)
) -> CommentBase:
    comment: Comment = Comment(
        author_id=user.id,
        photo_id=photo_id,
        text=text
    )

    db.add(comment)
    await db.commit()

    return CommentBase.from_orm(comment)

@comment_router.get('/get_all/')
async def get_all(
        db: db_dependency,
        photo_id: int
) -> List[CommentBase]:
    photo: Photo = await db.get(Photo, photo_id)
    return [CommentBase.from_orm(comment) for comment in photo.comments]


@comment_router.get('/get/')
async def get_one(
        db: db_dependency,
        comment_id: int
) -> PhotoBase:
    comment: Comment = await db.get(Comment, comment_id)
    return CommentBase.from_orm(comment)