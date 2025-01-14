from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from typing_extensions import Annotated


class CreatePost(BaseModel):
    title: str
    content: str

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
    id: Optional[int] = None

    class Config:
        from_attributes = True


class PostBase(BaseModel):
    id: int
    title: str
    content: str
    owner_id: int
    owner: UserBase

    class Config:
        from_attributes = True


class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(strict=True, le=1)]

    class Config:
        from_attributes = True


class PostVoteView(PostBase):
    votes: int

    class Config:
        from_attributes = True
