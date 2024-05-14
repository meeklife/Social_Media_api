from fastapi import FastAPI, HTTPException, status, Depends
from .utils import hash
from fastapi.params import Body
from random import randrange
from .models import Post
from . import models
from .database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from .schema import PostBase, CreatePost, UserBase, CreateUser
from typing import List

app = FastAPI()


models.Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts", response_model=List[PostBase])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=List[CreatePost])
def create_post(post: CreatePost, db: Session = Depends(get_db)):
    # new_post = models.Post(
    #     title=post.title, content=post.content)
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return [new_post]


@app.get("/posts/{id}", status_code=status.HTTP_200_OK, response_model=PostBase)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    if not deleted_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")

    deleted_post.delete(synchronize_session=False)
    db.commit()
    return {"messages": "Post successfully deleted"}


@app.put("/posts/{id}", response_model=List[CreatePost])
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


# Users route methods

@app.get("/users", response_model=List[UserBase])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@app.post("/users", response_model=List[UserBase])
def create_user(user: CreateUser, db: Session = Depends(get_db)):

    hashed_password = hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return [new_user]


@app.get("/users/{id}", response_model=UserBase)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User not found")

    return user
