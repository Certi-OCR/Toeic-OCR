import logging
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.common.error import BaseErrorResponse
from app.common.response import ErrorResponse


logger = logging.getLogger(__name__)


class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except BaseErrorResponse as http_exception:
            return JSONResponse(
                content=jsonable_encoder(
                    ErrorResponse(
                        status_code=http_exception.status_code,
                        message=http_exception.detail,
                    )
                ),
                status_code=http_exception.status_code,
                headers=http_exception.headers,
            )
        except RequestValidationError as validation_exception:
            return JSONResponse(
                status_code=422,
                content=jsonable_encoder(
                    ErrorResponse(
                        status_code=422,
                        message="Validation failed",
                        detail=validation_exception.errors(),
                        body=validation_exception.body,
                    )
                ),
            )
        except Exception as e:
            logger.exception(msg=e.__class__.__name__, args=e.args)
            return jsonable_encoder(
                ErrorResponse(
                    status_code=500,
                    message="Internal Error",
                )
            )
