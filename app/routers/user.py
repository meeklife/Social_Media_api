from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
from ..schema import UserBase, CreateUser
from ..database import get_db
from typing import List
from ..utils import hash
from .. import models
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/", response_model=List[UserBase])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.post("/", response_model=List[UserBase])
def create_user(user: CreateUser, db: Session = Depends(get_db)):

    hashed_password = hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return [new_user]


@router.get("/{id}", response_model=UserBase)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User not found")

    return user
