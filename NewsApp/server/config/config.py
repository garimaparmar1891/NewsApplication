from dotenv import load_dotenv
import os
from utils.api_key_loader import load_api_keys

api_keys = load_api_keys()

load_dotenv()

class Config:
    # App secrets
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    # API Keys
    NEWS_API_KEY = api_keys.get("newsapi")
    THENEWSAPI_TOKEN = api_keys.get("thenewsapi")

    # Database configuration
    DB_DRIVER = os.getenv("DB_DRIVER")
    DB_SERVER = os.getenv("DB_SERVER")
    DB_NAME = os.getenv("DB_NAME")
    DB_TRUSTED_CONNECTION = os.getenv("DB_TRUSTED_CONNECTION")

