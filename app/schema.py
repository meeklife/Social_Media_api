from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
    title: str
    content: str

    class Config:
        from_attributes = True


class CreatePost(PostBase):
    class Config:
        from_attributes = True


class CreateUser(BaseModel):
    email: EmailStr
    name: str
    password: str

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    id: int
    email: EmailStr
    name: str

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        from_attributes = True


class TokenData(BaseModel):
    id: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
