from pydantic import BaseModel, EmailStr
from datetime import datetime


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
