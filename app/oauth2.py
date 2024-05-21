from jose import JWTError, jwt
from datetime import datetime, timedelta
from .schema import TokenData
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({
        "exp": expire
    })

    encode_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

    return encode_jwt


def verify_access_token(token: str, credentials_exeption):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

        id: str = payload.get("user_id")
        if not id:
            raise credentials_exeption
        token_data = TokenData(id=id)

    except JWTError:
        raise credentials_exeption
