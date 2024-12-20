from datetime import date, datetime, timezone
from typing import Annotated
from beanie import Document, Indexed
from pydantic import Field
import pymongo


class Record(Document):
    name: str = Field(alias="name")
    id_number: str = Field(alias="id_number")
    date_of_birth: datetime = Field(
        default=datetime.now(timezone.utc), alias="date_of_birth"
    )
    test_date: Annotated[datetime, Indexed(index_type=pymongo.DESCENDING)] = Field(
        alias="test_date"
    )
    valid_until: datetime = Field(alias="valid_until")
    lis_score: int = Field(alias="lis_score", ge=0)
    read_score: int = Field(alias="read_score", ge=0)

    class Settings:
        name = "record"
        max_nesting_depth = 1
        schema_extra = {
            "example": {
                "_id": "string",
                "name": "John Doe",
                "id_number": "string",
                "date_of_birth": "2024-12-17 14:56:25.444698+00:00",
                "test_date": "2024-12-17 14:56:25.444698+00:00",
                "valid_until": "2024-12-17 14:56:25.444698+00:00",
                "lis_score": 230,
                "read_score": 205,
            }
        }
