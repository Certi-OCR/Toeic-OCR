from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import HTTPException, status
from jose import JWTError, jwt
from app.common.error import Unauthorized
from app.schemas.user import TokenData
from app.core.config.config import Config

SECRET_KEY = Config.app_settings.get("secret_key")
ALGORITHM = Config.app_settings.get("algorithm")
ACCESS_TOKEN_EXPIRE_MINUTES = Config.app_settings.get("access_token_expire_minutes")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str):
    from passlib.context import CryptContext

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    check = pwd_context.verify(secret=plain_password, hash=hashed_password)
    print(check)
    return check


def get_password_hash(password: str):
    from passlib.context import CryptContext

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)


def decode_access_token(token: str):
    credentials_exception = Unauthorized(
        message="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("sub")
        if id is None:
            raise credentials_exception
        token_data = TokenData(id == id)
    except JWTError:
        raise credentials_exception
    return token_data
