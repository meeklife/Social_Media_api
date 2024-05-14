from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
from fastapi.params import Body
from random import randrange
from ..models import Post
from ..schema import PostBase, CreatePost
from ..database import get_db
from typing import List
from ..utils import hash
from .. import models
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", response_model=List[PostBase])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=List[CreatePost])
def create_post(post: CreatePost, db: Session = Depends(get_db)):
    # new_post = models.Post(
    #     title=post.title, content=post.content)
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return [new_post]


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=PostBase)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    if not deleted_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")

    deleted_post.delete(synchronize_session=False)
    db.commit()
    return {"messages": "Post successfully deleted"}


@router.put("/{id}", response_model=List[CreatePost])
def update_post(id: int, post: CreatePost, db: Session = Depends(get_db)):
    updated_post = db.query(models.Post).filter(models.Post.id == id)
    posts = updated_post.first()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")

    updated_post.update(post.model_dump(), synchronize_session=False)

    db.add(posts)
    db.commit()

    return [updated_post.first()]
