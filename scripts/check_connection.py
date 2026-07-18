import sys
from pathlib import Path

from sqlalchemy import text

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app import app
from portfolio.extensions import db

with app.app_context():
    result = db.session.execute(text("SELECT 1 AS connection_ok")).scalar_one()
    print(f"Koneksi database berhasil. Hasil SELECT 1 = {result}")
