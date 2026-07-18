import os
from pathlib import Path

import certifi
from dotenv import load_dotenv
from sqlalchemy.engine import URL

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def required_env(name: str) -> str:
    """Mengambil environment variable wajib tanpa menampilkan nilainya."""
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(
            f"Environment variable {name} belum diisi. "
            "Tambahkan nilainya di .env lokal atau Vercel Project Settings."
        )
    return value


def build_database_uri() -> str:
    """Membangun URI database dari DATABASE_URL atau kredensial TiDB."""
    database_url = os.getenv("DATABASE_URL", "").strip()
    if database_url:
        return database_url

    return URL.create(
        drivername="mysql+pymysql",
        username=required_env("TIDB_USERNAME"),
        password=required_env("TIDB_PASSWORD"),
        host=required_env("TIDB_HOST"),
        port=int(os.getenv("TIDB_PORT", "4000")),
        database=required_env("TIDB_DATABASE"),
        query={"charset": "utf8mb4"},
    ).render_as_string(hide_password=False)


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "development-secret-key-change-this")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 280,
        "pool_size": 2,
        "max_overflow": 1,
        "pool_timeout": 10,
        "connect_args": {
            "connect_timeout": 20,
            "read_timeout": 20,
            "write_timeout": 20,
            "ssl": {"ca": certifi.where()},
        },
    }

    # Vercel Functions membatasi payload request/response hingga 4,5 MB.
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", str(4 * 1024 * 1024)))

    IS_PRODUCTION = (
        os.getenv("VERCEL_ENV", "").lower() == "production"
        or os.getenv("FLASK_ENV", "").lower() == "production"
    )
    SESSION_COOKIE_SECURE = IS_PRODUCTION
    REMEMBER_COOKIE_SECURE = IS_PRODUCTION
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    REMEMBER_COOKIE_SAMESITE = "Lax"

    CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME", "")
    CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY", "")
    CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET", "")

    RESEND_API_KEY = os.getenv("RESEND_API_KEY", "")
    RESEND_FROM = os.getenv("RESEND_FROM", "Portfolio <onboarding@resend.dev>")
    CONTACT_RECEIVER_EMAIL = os.getenv("CONTACT_RECEIVER_EMAIL", "")

    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "")


def apply_runtime_config(app) -> None:
    """Melengkapi konfigurasi yang harus dibaca saat aplikasi dibuat."""
    if not app.config.get("SQLALCHEMY_DATABASE_URI"):
        app.config["SQLALCHEMY_DATABASE_URI"] = build_database_uri()

    if app.config.get("TESTING"):
        return

    if app.config.get("IS_PRODUCTION") and app.config.get("SECRET_KEY") == "development-secret-key-change-this":
        raise RuntimeError(
            "SECRET_KEY produksi belum aman. Buat nilai acak dan simpan sebagai "
            "Environment Variable di Vercel."
        )
