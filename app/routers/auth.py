from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from ..database import get_db
from ..schema import UserLogin
from ..models import User
from ..utils import verify_password
from ..oauth2 import create_access_token

router = APIRouter(tags=['Authentication'])


@router.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(
        User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Invalid credentials')

    verified_password = verify_password(
        user_credentials.password, user.password)

    if not verified_password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Invalid credentials')

    access_token = create_access_token(data={"user_id": user.id})

    # create a token
    return {"access_token": access_token, "token_type": "bearer"}
