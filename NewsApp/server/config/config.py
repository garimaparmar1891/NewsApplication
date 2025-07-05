from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
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

    @staticmethod
    def validate():
        required = [
            Config.SECRET_KEY,
            Config.JWT_SECRET_KEY,
            Config.DB_DRIVER,
            Config.DB_SERVER,
            Config.DB_NAME,
            Config.DB_TRUSTED_CONNECTION,
            Config.SMTP_SERVER,
            Config.SMTP_PORT,
            Config.SMTP_USERNAME,
            Config.SMTP_PASSWORD,
            Config.SMTP_SENDER,
        ]
        missing = [name for name, value in zip([
            "SECRET_KEY", "JWT_SECRET_KEY", "DB_DRIVER", "DB_SERVER", "DB_NAME", "DB_TRUSTED_CONNECTION",
            "SMTP_SERVER", "SMTP_PORT", "SMTP_USERNAME", "SMTP_PASSWORD", "SMTP_SENDER"
        ], required) if value is None]
        if missing:
            raise ValueError(f"Missing required config variables: {', '.join(missing)}")
