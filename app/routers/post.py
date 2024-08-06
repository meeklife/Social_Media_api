from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
from fastapi.params import Body
from random import randrange
from app.models import Post
from app.schema import PostBase, CreatePost, PostVoteView
from app.database import get_db
from typing import List, Optional
from app.utils import hash
from app import models
from app.oauth2 import get_current_user
from sqlalchemy import func
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", response_model=List[PostVoteView])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ''):
    posts = db.query(models.Post).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()

    results = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(
        models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()

    posts = []
    for post, votes in results:
        post_dict = {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "owner_id": post.owner_id,
            "owner": post.owner,
            "votes": votes
        }
        posts.append(post_dict)

    return posts


@router.get("/myposts", response_model=List[PostBase])
def get_users_posts(db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    posts = db.query(models.Post).filter(
        models.Post.owner_id == current_user.id).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=List[CreatePost])
def create_post(post: CreatePost, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return [new_post]


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=PostVoteView)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post_query = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(
        models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id)

    result = post_query.first()

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
    post, votes = result

    return {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "owner_id": post.owner_id,
        "owner": post.owner,
        "votes": votes
    }


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    post = deleted_post.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to delete this post")

    deleted_post.delete(synchronize_session=False)
    db.commit()
    return {"messages": "Post successfully deleted"}


@router.patch("/{id}", response_model=List[CreatePost])
def update_post(id: int, post: CreatePost, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    updated_post = db.query(models.Post).filter(models.Post.id == id)
    posts = updated_post.first()

    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")

    if posts.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to update this post")

    updated_post.update(post.model_dump(), synchronize_session=False)

    db.add(posts)
    db.commit()

    return [updated_post.first()]
