from datetime import datetime, timezone

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db


def utc_now():
    return datetime.now(timezone.utc).replace(tzinfo=None)


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.BigInteger().with_variant(db.Integer, "sqlite"), primary_key=True)
    email = db.Column(db.String(190), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(30), nullable=False, default="admin")
    created_at = db.Column(db.DateTime, nullable=False, default=utc_now)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Profile(db.Model):
    __tablename__ = "profiles"

    id = db.Column(db.BigInteger().with_variant(db.Integer, "sqlite"), primary_key=True)
    brand_name = db.Column(db.String(100), nullable=False, default="DevPortfolio")
    full_name = db.Column(db.String(150), nullable=False, default="Nama Lengkap")
    headline = db.Column(db.String(220), nullable=False, default="Web Developer & UI/UX Enthusiast")
    short_intro = db.Column(db.Text, nullable=False)
    availability_text = db.Column(db.String(120), nullable=False, default="Available for freelance")
    about_text = db.Column(db.Text, nullable=False)
    about_text_secondary = db.Column(db.Text, nullable=False)
    years_experience = db.Column(db.String(30), nullable=False, default="5+")
    email = db.Column(db.String(190), nullable=False)
    phone = db.Column(db.String(60), nullable=False)
    location = db.Column(db.String(160), nullable=False)
    education = db.Column(db.String(160), nullable=False)
    work_status = db.Column(db.String(100), nullable=False, default="Open for Work")
    github_url = db.Column(db.String(500), nullable=True)
    linkedin_url = db.Column(db.String(500), nullable=True)
    hero_image_url = db.Column(db.String(1000), nullable=True)
    hero_image_public_id = db.Column(db.String(300), nullable=True)
    about_image_url = db.Column(db.String(1000), nullable=True)
    about_image_public_id = db.Column(db.String(300), nullable=True)
    cv_url = db.Column(db.String(1000), nullable=True)
    cv_public_id = db.Column(db.String(300), nullable=True)
    footer_text = db.Column(db.String(255), nullable=False, default="Web Developer & UI/UX Enthusiast")
    updated_at = db.Column(db.DateTime, nullable=False, default=utc_now, onupdate=utc_now)


class Skill(db.Model):
    __tablename__ = "skills"

    id = db.Column(db.BigInteger().with_variant(db.Integer, "sqlite"), primary_key=True)
    category = db.Column(db.String(100), nullable=False)
    icon = db.Column(db.String(80), nullable=False, default="code")
    items = db.Column(db.Text, nullable=False)
    sort_order = db.Column(db.Integer, nullable=False, default=0)

    @property
    def item_list(self):
        return [item.strip() for item in self.items.splitlines() if item.strip()]


class Experience(db.Model):
    __tablename__ = "experiences"

    id = db.Column(db.BigInteger().with_variant(db.Integer, "sqlite"), primary_key=True)
    period = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(180), nullable=False)
    organization = db.Column(db.String(180), nullable=False)
    description = db.Column(db.Text, nullable=False)
    item_type = db.Column(db.String(30), nullable=False, default="experience")
    sort_order = db.Column(db.Integer, nullable=False, default=0)
    is_active = db.Column(db.Boolean, nullable=False, default=False)


class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.BigInteger().with_variant(db.Integer, "sqlite"), primary_key=True)
    title = db.Column(db.String(180), nullable=False)
    description = db.Column(db.Text, nullable=False)
    technologies = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(1000), nullable=True)
    image_public_id = db.Column(db.String(300), nullable=True)
    live_url = db.Column(db.String(1000), nullable=True)
    code_url = db.Column(db.String(1000), nullable=True)
    is_featured = db.Column(db.Boolean, nullable=False, default=True)
    sort_order = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, nullable=False, default=utc_now)

    @property
    def tech_list(self):
        normalized = self.technologies.replace(",", "\n")
        return [item.strip() for item in normalized.splitlines() if item.strip()]


class ContactMessage(db.Model):
    __tablename__ = "contact_messages"

    id = db.Column(db.BigInteger().with_variant(db.Integer, "sqlite"), primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(190), nullable=False, index=True)
    subject = db.Column(db.String(220), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=utc_now, index=True)
