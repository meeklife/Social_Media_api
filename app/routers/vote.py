from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from app.models import Votes, Post
from app.database import get_db
from app.oauth2 import get_current_user
from app.schema import Vote

router = APIRouter(
    prefix="/vote",
    tags=["Votes"]
)

# , response_model = Vote


@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(vote: Vote, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):

    post = db.query(Post).filter(Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {vote.post_id} does not exist')

    vote_query = db.query(Votes).filter(
        Votes.post_id == vote.post_id, Votes.user_id == current_user.id)
    found_vote = vote_query.first()

    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f'user {current_user.id} has already voted on post {vote.post_id}')
        new_vote = Votes(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {
            'message': 'Succesfully added vote'
        }
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f'vote does not exist')

        vote_query.delete(synchronize_session=False)
        db.commit()
        return {
            'message': 'Successfully deleted vote'
        }
