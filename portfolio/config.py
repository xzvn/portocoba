import os
from pathlib import Path
from urllib.parse import quote_plus

import certifi
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


def _database_config():
    database_url = os.getenv("DATABASE_URL", "").strip()
    if database_url:
        if database_url.startswith("mysql://"):
            database_url = database_url.replace("mysql://", "mysql+pymysql://", 1)
        if database_url.startswith("sqlite"):
            return database_url, {"connect_args": {"check_same_thread": False}}
        return database_url, {
            "pool_pre_ping": True,
            "pool_recycle": 280,
            "connect_args": {"ssl": {"ca": certifi.where()}},
        }

    host = os.getenv("TIDB_HOST", "").strip()
    if host:
        port = int(os.getenv("TIDB_PORT", "4000"))
        username = quote_plus(os.getenv("TIDB_USERNAME", ""))
        password = quote_plus(os.getenv("TIDB_PASSWORD", ""))
        database = os.getenv("TIDB_DATABASE", "portfolio")
        uri = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}?charset=utf8mb4"
        return uri, {
            "pool_pre_ping": True,
            "pool_recycle": 280,
            "connect_args": {"ssl": {"ca": certifi.where()}},
        }

    sqlite_path = BASE_DIR / "portfolio_local.db"
    return f"sqlite:///{sqlite_path.as_posix()}", {
        "connect_args": {"check_same_thread": False}
    }


DATABASE_URI, ENGINE_OPTIONS = _database_config()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "local-only-change-this-secret")
    SQLALCHEMY_DATABASE_URI = DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = ENGINE_OPTIONS
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = os.getenv("VERCEL", "") == "1" or os.getenv("FLASK_ENV") == "production"
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SAMESITE = "Lax"
    REMEMBER_COOKIE_SECURE = SESSION_COOKIE_SECURE

    CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME", "")
    CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY", "")
    CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET", "")

    RESEND_API_KEY = os.getenv("RESEND_API_KEY", "")
    RESEND_FROM = os.getenv("RESEND_FROM", "Portfolio <onboarding@resend.dev>")
    CONTACT_RECEIVER_EMAIL = os.getenv("CONTACT_RECEIVER_EMAIL", "")
