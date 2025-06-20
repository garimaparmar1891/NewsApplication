from dotenv import load_dotenv
import os
from repositories.external_server_repository import ExternalServerRepository

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    external_keys = ExternalServerRepository().get_keys()
    NEWS_API_KEY = external_keys.get("NewsAPI", {}).get("api_key")
    THENEWSAPI_TOKEN = external_keys.get("TheNewsAPI", {}).get("api_key")

    DB_DRIVER = os.getenv("DB_DRIVER")
    DB_SERVER = os.getenv("DB_SERVER")
    DB_NAME = os.getenv("DB_NAME")
    DB_TRUSTED_CONNECTION = os.getenv("DB_TRUSTED_CONNECTION")

    FETCH_INTERVAL_HOURS = int(os.getenv("FETCH_INTERVAL_HOURS", 3))

    SMTP_SERVER = os.getenv("SMTP_SERVER")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
    SMTP_USERNAME = os.getenv("SMTP_USERNAME")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
    SMTP_SENDER = os.getenv("SMTP_SENDER")
