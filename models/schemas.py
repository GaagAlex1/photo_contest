from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class ContestCreateBase(BaseModel):
    name: str
    owner_id: int


class ContestBase(BaseModel):
    id: int
    name: str
    owner_id: int

    class Config:
        from_attributes = True


class PhotoCreateBase(BaseModel):
    url: str
    author_id: int
    contest_id: int


class PhotoBase(BaseModel):
    id: int
    url: str
    author_id: int
    contest_id: int

    class Config:
        from_attributes = True


class CommentCreateBase(BaseModel):
    photo_id: int
    author_id: int
    text: str


class CommentBase(BaseModel):
    id: int
    photo_id: int
    author_id: int
    text: str

    class Config:
        from_attributes = True


class VoteCreateBase(BaseModel):
    photo_id: int
    author_id: int
    rate: int


class VoteBase(BaseModel):
    id: int
    photo_id: int
    author_id: int
    rate: int

    class Config:
        from_attributes = True
