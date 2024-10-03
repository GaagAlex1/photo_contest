from typing import Annotated
from fastapi import APIRouter, Depends, Response, HTTPException, status, Request, Body, Cookie
from sqlalchemy import select
from auth.utils import *
from models.orm import User
from auth.schemas import UserCreateBase, UserBase, TokenInfo
from database import db_dependency
import jwt

auth_router = APIRouter(prefix='/auth')


@auth_router.post('/register')
async def register(user: UserCreateBase, db: db_dependency) -> UserBase:
    new_user = User(
        email=user.email,
        hashed_password=hash_passwd(user.password),
        nickname=user.nickname,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return UserBase.from_orm(new_user)


async def validate_auth_user(
        db: db_dependency,
        email: str = Body(..., embed=True),
        password: str = Body(..., embed=True)
) -> UserBase | None:
    stmt = select(User).filter(User.email == email)
    user: User = (await db.execute(stmt)).scalars().one_or_none()
    if user is None or not validate_passwd(password, user.hashed_password):
        raise HTTPException(
            status_code=403,
            detail='User doesn`t exist or password is invalid'
        )
    return UserBase.from_orm(user)


def create_access_token(user: UserBase) -> str:
    payload: dict = {
        'id': user.id,
        'email': user.email
    }
    access_token: str = encode_jwt(payload, expire_minutes=1)
    return access_token


def create_refresh_token(user: UserBase) -> str:
    payload: dict = {
        'id': user.id
    }
    refresh_token: str = encode_jwt(payload, expire_minutes=43200)
    return refresh_token


@auth_router.post('/login', response_model=TokenInfo)
async def login(
        response: Response,
        user: UserBase = Depends(validate_auth_user)
) -> TokenInfo:
    access_token: str = create_access_token(user)
    refresh_token: str = create_refresh_token(user)
    response.set_cookie(key='access-token', value=f'{access_token}', httponly=True)
    response.set_cookie(key='refresh-token', value=f'{refresh_token}', httponly=True)

    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token
    )


@auth_router.get('/users/me', response_model=UserBase)
async def get_cur_auth_user(
        db: db_dependency,
        access_token: str | None = Cookie(default=None, alias='access-token')
) -> UserBase | None:
    try:
        payload: dict = decode_jwt(access_token)
        user_id: int = payload.get('id')
        if id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        user: User = await db.get(User, user_id)
        return UserBase.from_orm(user)
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED
        )


@auth_router.post('/refresh')
async def refresh(
        db: db_dependency,
        response: Response,
        refresh_token: str | None = Cookie(default=None, alias='refresh-token')
) -> TokenInfo | None:
    try:
        payload: dict = decode_jwt(refresh_token)
        user_id: int = payload.get('id')
        user_orm: User = await db.get(User, user_id)
        user: UserBase = UserBase.from_orm(user_orm)

        access_token: str = create_access_token(user)
        refresh_token: str = create_refresh_token(user)
        response.set_cookie(key='access-token', value=f'{access_token}', httponly=True)
        response.set_cookie(key='refresh-token', value=f'{refresh_token}', httponly=True)

        return TokenInfo(
            access_token=access_token,
            refresh_token=refresh_token
        )

    except jwt.PyJWTError:
        raise HTTPException(
            status_code=401,
            detail='Refresh token is expired, please log in again'
        )


user_dependency = Annotated[UserBase, Depends(get_cur_auth_user)]