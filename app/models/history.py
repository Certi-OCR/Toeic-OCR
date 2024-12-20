from datetime import date, datetime, timezone
from beanie import BeanieObjectId, Document, Link
from bson import ObjectId
from pydantic import Field

from app.models.record import Record
from app.models.user import User


class History(Document):
    record: Link[Record]
    created_by: Link[User]
    created_at: datetime = Field(default=datetime.now(timezone.utc), alias="created_at")

    class Settings:
        name = "history"
        max_nesting_depth = 1
        schema_extra = {
            "example": {
                "_id": "string",
                "record": {
                    "_id": "string",
                    "name": "John Doe",
                    "id_number": "string",
                    "date_of_birth": "2024-12-17 14:56:25.444698+00:00",
                    "test_date": "2024-12-17 14:56:25.444698+00:00",
                    "valid_until": "2024-12-17 14:56:25.444698+00:00",
                    "lis_score": 230,
                    "read_score": 205,
                },
                "created_by": {
                    "_id": "string",
                    "email": "johndoe@gmail.com",
                    "full_name": "John Doe",
                    "hashed_password": "string",
                    "disabled": False,
                    "created_at": "2024-12-17 14:56:25.444698+00:00",
                },
                "created_at": "2024-12-17 14:56:25.444698+00:00",
            }
        }
