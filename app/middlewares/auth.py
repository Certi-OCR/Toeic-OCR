from functools import wraps
from fastapi import Request, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.common.error import Unauthorized
from app.common.response import ErrorResponse
from app.core.auth.jwt import decode_access_token


def auth_guard(handler):
    @wraps(handler)
    async def dispatch(self, request: Request, call_next):
        token = request.headers.get("Authorization")
        if not token:
            return JSONResponse(
                status_code=401,
                headers={"WWW-Authenticate": "Bearer"},
                content=jsonable_encoder(
                    ErrorResponse(status_code=401, message="Not authenticated")
                ),
            )
        try:
            token_data = decode_access_token(token.split(" ")[1])
        except Exception as e:
            return JSONResponse(
                status_code=401,
                headers={"WWW-Authenticate": "Bearer"},
                content=jsonable_encoder(
                    ErrorResponse(status_code=401, message="Not authenticated")
                ),
            )

        response = await call_next(request)
        return response
