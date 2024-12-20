from typing import Optional, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class SuccessResponse[T](BaseModel):
    status_code: Optional[int] = None
    message: Optional[str] = None
    data: Optional[T] = None

    def __init__(
        self,
        status_code: Optional[int] = None,
        message: Optional[str] = None,
        data: Optional[T] = None,
    ):
        super().__init__()
        self.status_code = status_code
        self.message = message
        self.data = data


class ErrorResponse[T](BaseModel):
    status_code: Optional[int] = None
    message: Optional[str] = None
    detail: Optional[list] = None
    body: Optional[T] = None

    def __init__(
        self,
        status_code: Optional[int] = None,
        message: Optional[str] = None,
        detail: Optional[list] = None,
        body: Optional[T] = None,
    ):
        super().__init__()
        self.status_code = status_code
        self.message = message
        self.detail = detail
        self.body = body
