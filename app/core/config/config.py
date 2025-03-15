import os
from dotenv import load_dotenv
import logging

from fastapi import HTTPException, status

load_dotenv()


class Config:
    version = "0.1.0"
    title = "releases"

    app_settings = {}

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
