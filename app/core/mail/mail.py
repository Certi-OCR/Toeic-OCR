from fastapi_mail import ConnectionConfig, FastMail

from app.core.config.config import Config


def init_mail_service():
    config = ConnectionConfig(
        MAIL_FROM=Config.app_settings.get("email_user"),
        MAIL_PASSWORD=Config.app_settings.get("email_pwd"),
        MAIL_SERVER=Config.app_settings.get("email_host"),
        MAIL_STARTTLS=False,
        MAIL_SSL_TLS=True,
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=True,
    )
    return FastMail(config)
