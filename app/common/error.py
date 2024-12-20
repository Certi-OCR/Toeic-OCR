import logging
from typing import Optional
from starlette.exceptions import HTTPException as StarletteHTTPException


class BaseErrorResponse(StarletteHTTPException):
    def __init__(
        self, status: int, detail: str, headers: Optional[dict] = None
    ) -> None:
        self.status_code = status
        self.detail = detail
        self.headers = headers


class BadRequest(BaseErrorResponse):
    def __init__(self, message: Optional[str] = None, headers: Optional[dict] = None):
        super(BadRequest, self).__init__(400, message or "Bad Request", headers)


class NotFound(BaseErrorResponse):
    def __init__(self, message: Optional[str] = None, headers: Optional[dict] = None):
        super(NotFound, self).__init__(404, message or "Not found", headers)


class Unauthorized(BaseErrorResponse):
    def __init__(self, message: Optional[str] = None, headers: Optional[dict] = None):
        super(Unauthorized, self).__init__(401, message or "Unauthorized", headers)


class Forbidden(BaseErrorResponse):
    def __init__(self, message: Optional[str] = None, headers: Optional[dict] = None):
        super(Forbidden, self).__init__(403, message or "Forbidden", headers)


class UnprocessableError(BaseErrorResponse):
    def __init__(self, message: Optional[str] = None, headers: Optional[dict] = None):
        super(UnprocessableError, self).__init__(
            422, message or "Unprocessable Entity", headers
        )


class InternalError(BaseErrorResponse):
    def __init__(self, message: Optional[str] = None, headers: Optional[dict] = None):
        super(InternalError, self).__init__(500, message or "Internal Error", headers)
