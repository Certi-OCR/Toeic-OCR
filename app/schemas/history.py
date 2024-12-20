from datetime import date
from pydantic import BaseModel

from app.schemas.record import RecordOut
from app.schemas.user import UserOut


class HistoryOut(BaseModel):
    id: str
    record: RecordOut
    created_by: UserOut
    created_at: date


class HistoryCreate(BaseModel):
    id: str
    record: RecordOut
    created_by: UserOut
    created_at: date
