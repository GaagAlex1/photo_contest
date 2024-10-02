from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from typing import List
from database import Base


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    nickname: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[bytes]

    created_contests: Mapped[List['Contest']] = relationship('Contest', back_populates='owner', lazy='selectin')
    participated_contests: Mapped[List['Contest']] = relationship(back_populates='participants',
                                                                  secondary='user_contest', lazy='selectin')
    photos: Mapped[List['Photo']] = relationship('Photo', back_populates='author', lazy='selectin')
    comments: Mapped[List['Comment']] = relationship('Comment', back_populates='author', lazy='selectin')
    votes: Mapped[List['Vote']] = relationship('Vote', back_populates='author', lazy='selectin')


class Contest(Base):
    __tablename__ = 'contest'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    owner_id: Mapped[int] = mapped_column(ForeignKey('user.id'))

    owner: Mapped['User'] = relationship('User', back_populates='created_contests', lazy='selectin')
    participants: Mapped[List['User']] = relationship(back_populates='participated_contests',
                                                      secondary='user_contest', lazy='selectin')
    photos: Mapped[List['Photo']] = relationship('Photo', back_populates='contest', lazy='selectin')


class UserContest(Base):
    __tablename__ = 'user_contest'
    participant_id: Mapped[int] = mapped_column(ForeignKey('user.id'), primary_key=True)
    contest_id: Mapped[int] = mapped_column(ForeignKey('contest.id'), primary_key=True)


class Photo(Base):
    __tablename__ = 'photo'
    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    contest_id: Mapped[int] = mapped_column(ForeignKey('contest.id'))
    url: Mapped[str]

    contest: Mapped['Contest'] = relationship('Contest', back_populates='photos', lazy='selectin')
    author: Mapped['User'] = relationship('User', back_populates='photos', lazy='selectin')
    votes: Mapped[List['Vote']] = relationship('Vote', back_populates='photo', lazy='selectin')
    comments: Mapped[List['Comment']] = relationship('Comment', back_populates='photo', lazy='selectin')


class Vote(Base):
    __tablename__ = 'vote'

    id: Mapped[int] = mapped_column(primary_key=True)
    photo_id: Mapped[int] = mapped_column(ForeignKey('photo.id'))
    author_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    rate: Mapped[int]

    photo: Mapped['Photo'] = relationship('Photo', back_populates='votes', lazy='selectin')
    author: Mapped['User'] = relationship('User', back_populates='votes', lazy='selectin')


class Comment(Base):
    __tablename__ = 'comment'

    id: Mapped[int] = mapped_column(primary_key=True)
    photo_id: Mapped[int] = mapped_column(ForeignKey('photo.id'))
    author_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    text: Mapped[str]

    photo: Mapped['Photo'] = relationship('Photo', back_populates='comments', lazy='selectin')
    author: Mapped['User'] = relationship('User', back_populates='comments', lazy='selectin')
