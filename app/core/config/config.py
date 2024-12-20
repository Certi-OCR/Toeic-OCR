import os
from dotenv import load_dotenv
import logging

from fastapi import HTTPException, status

load_dotenv()


class Config:
    version = "0.1.0"
    title = "releases"

    app_settings = {
        "db_name": os.getenv("DATABASE_NAME"),
        "db_url": os.getenv("DATABASE_URL"),
        "secret_key": os.getenv("SECRET_KEY", "secret"),
        "algorithm": "HS256",
        "access_token_expire_minutes": int(
            os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
        ),
        "refresh_token_expire_days": int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 10)),
        "email_host": os.getenv("EMAIL_HOST"),
        "email_user": os.getenv("EMAIL_USER"),
        "email_pwd": os.getenv("EMAIL_PWD"),
    }

    @classmethod
    def app_settings_validate(cls):
        for k, v in cls.app_settings.items():
            if None is v:
                logging.error(f"Config variable error. {k} cannot be None")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Server configure error",
                )
            else:
                logging.info(f"Config variable {k} is {v}")
