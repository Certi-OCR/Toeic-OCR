from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.common.error import BadRequest, BaseErrorResponse, Unauthorized
from app.core.auth.jwt import create_access_token
from app.core.db.db import get_db
from app.common.response import SuccessResponse

# from app.middlewares.auth import AuthMiddleware
from app.services.user import authenticate_user
from app.dependencies.auth import get_current_active_user
from app.schemas.user import Token, UserOut


router = APIRouter()


@router.post("/login", response_model=SuccessResponse[Token], status_code=200)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise BadRequest(
            message="Incorrect username or password",
        )
    access_token = create_access_token(data={"sub": str(user.id)})
    return SuccessResponse(
        data={"access_token": access_token, "token_type": "bearer"},
        status_code=200,
        message="Log in successfully",
    )


@router.get(
    "/me",
    response_model=SuccessResponse[UserOut],
    status_code=200,
)
async def read_users_me(current_user: UserOut = Depends(get_current_active_user)):
    return SuccessResponse(
        data=current_user,
        status_code=200,
        message="Get user's information successfully",
    )


# @router.post("/reset-password", response_model=Response, status_code=200)
# async def reset_password()
