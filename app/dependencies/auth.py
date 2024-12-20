from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from app.common.error import BadRequest, Unauthorized
from app.core.auth.jwt import decode_access_token
from app.core.db.db import get_db
from app.models.user import User
from app.services.user import get_user_by_id
from motor.motor_asyncio import AsyncIOMotorDatabase

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = Unauthorized(
        message="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token_data = decode_access_token(token)
    except JWTError:
        raise credentials_exception
    user = await get_user_by_id(token_data.id)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise BadRequest(message="Inactive user")
    return current_user
