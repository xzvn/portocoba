import pytest

from portfolio import create_app
from portfolio.extensions import db
from portfolio.models import Profile


class TestConfig:
    TESTING = True
    SECRET_KEY = "test-secret"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"connect_args": {"check_same_thread": False}}
    WTF_CSRF_ENABLED = False
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024
    CLOUDINARY_CLOUD_NAME = ""
    CLOUDINARY_API_KEY = ""
    CLOUDINARY_API_SECRET = ""
    RESEND_API_KEY = ""
    RESEND_FROM = ""
    CONTACT_RECEIVER_EMAIL = ""
    SESSION_COOKIE_SECURE = False
    REMEMBER_COOKIE_SECURE = False


@pytest.fixture()
def client():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        db.session.add(Profile(
            brand_name="Test Portfolio", full_name="Test User", headline="Developer",
            short_intro="Intro", availability_text="Available", about_text="About",
            about_text_secondary="More", years_experience="1+", email="test@example.com",
            phone="123", location="Indonesia", education="S1", work_status="Open",
            footer_text="Developer"
        ))
        db.session.commit()
    return app.test_client()


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Test Portfolio" in response.data


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"
