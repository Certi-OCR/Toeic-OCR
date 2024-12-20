from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class RecordOut(BaseModel):
    id: str
    name: str
    id_number: str
    date_of_birth: datetime
    test_date: datetime
    valid_until: datetime
    lis_score: int
    read_score: int


class RecordCreate(BaseModel):
    name: str
    id_number: str
    date_of_birth: datetime
    test_date: datetime
    valid_until: datetime
    lis_score: int
    read_score: int


class RecordUpdate(BaseModel):
    name: Optional[str]
    id_number: Optional[str]
    date_of_birth: Optional[datetime]
    test_date: Optional[datetime]
    valid_until: Optional[datetime]
    lis_score: Optional[int]
    read_score: Optional[int]
