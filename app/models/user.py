from datetime import date, datetime, timezone
from beanie import Document
from bson import ObjectId, Timestamp
from pydantic import EmailStr, Field
from typing import Optional


class User(Document):
    username: str = Field(alias="username")
    email: str = Field(alias="email")
    full_name: Optional[str] = Field(default=None, alias="full_name")
    hashed_password: str = Field(alias="hashed_password")
    disabled: Optional[bool] = Field(default=None, alias="disabled")
    created_at: datetime = Field(default=datetime.now(timezone.utc), alias="created_at")

    class Settings:
        name = "user"
        schema_extra = {
            "example": {
                "_id": "string",
                "username": "lvakhoa",
                "email": "johndoe@gmail.com",
                "full_name": "John Doe",
                "hashed_password": "$2a$10$WRFDS3aBGTNqSvl3pfX2DO2xkoRLfnNdJzrIMs9NFthI1cUPg2Q4O",  # abcd
                "disabled": False,
                "created_at": "2024-12-17 14:56:25.444698+00:00",
            }
        }
