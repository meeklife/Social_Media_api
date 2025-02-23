from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.schema import TokenData
from app.models import User
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db

oAuth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({
        "exp": expire
    })

    encode_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

    return encode_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: int = payload.get("user_id")
        if not id:
            raise credentials_exception
        token_data = TokenData(id=id)

    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oAuth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = verify_access_token(token, credentials_exception)

    user = db.query(User).filter(User.id == token.id).first()

    return user
