import os
from pathlib import Path

import certifi
from dotenv import load_dotenv
from sqlalchemy.engine import URL

load_dotenv()

# Folder utama proyek: D:\portfolio_stitch
BASE_DIR = Path(__file__).resolve().parent.parent

# Memuat file D:\portfolio_stitch\.env
load_dotenv(BASE_DIR / ".env")


def required_env(name: str) -> str:
    """Mengambil environment variable wajib."""
    value = os.getenv(name)

    if not value:
        raise RuntimeError(
            f"Environment variable {name} belum diisi. "
            f"Periksa file: {BASE_DIR / '.env'}"
        )

    return value


class Config:
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "development-secret-key-change-this",
    )

    TIDB_HOST = required_env("TIDB_HOST")
    TIDB_PORT = int(os.getenv("TIDB_PORT", "4000"))
    TIDB_USERNAME = required_env("TIDB_USERNAME")
    TIDB_PASSWORD = required_env("TIDB_PASSWORD")
    TIDB_DATABASE = required_env("TIDB_DATABASE")

    SQLALCHEMY_DATABASE_URI = URL.create(
         drivername="mysql+pymysql",
        username=os.environ["TIDB_USERNAME"].strip(),
        password=os.environ["TIDB_PASSWORD"],
        host=os.environ["TIDB_HOST"].strip(),
        port=int(os.getenv("TIDB_PORT", "4000")),
        database=os.environ["TIDB_DATABASE"].strip(),
        query={"charset": "utf8mb4"},
    ).render_as_string(hide_password=False)

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 280,
        "connect_args": {
            "connect_timeout": 20,
            "read_timeout": 20,
            "write_timeout": 20,
            "ssl": {
                "ca": certifi.where(),
            }
        },
    }

    CLOUDINARY_CLOUD_NAME = os.getenv(
        "CLOUDINARY_CLOUD_NAME",
        "",
    )
    CLOUDINARY_API_KEY = os.getenv(
        "CLOUDINARY_API_KEY",
        "",
    )
    CLOUDINARY_API_SECRET = os.getenv(
        "CLOUDINARY_API_SECRET",
        "",
    )

    RESEND_API_KEY = os.getenv("RESEND_API_KEY", "")
    RESEND_FROM = os.getenv(
        "RESEND_FROM",
        "Portofolio <onboarding@resend.dev>",
    )
    CONTACT_RECEIVER_EMAIL = os.getenv(
        "CONTACT_RECEIVER_EMAIL",
        "",
    )

    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "")