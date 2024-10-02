from pydantic import BaseModel, EmailStr


class UserCreateBase(BaseModel):
    email: EmailStr
    password: str
    nickname: str


class UserBase(BaseModel):
    id: int
    email: EmailStr
    nickname: str

    class Config:
        from_attributes = True


class TokenInfo(BaseModel):
    access_token: bytes
    refresh_token: bytes
    type: str = 'Bearer'