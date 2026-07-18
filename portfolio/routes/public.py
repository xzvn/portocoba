from email.utils import parseaddr

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for

from ..extensions import db
from ..models import ContactMessage, Experience, Profile, Project, Skill
from ..services.email_service import send_contact_notification

public_bp = Blueprint("public", __name__)


@public_bp.get("/")
def home():
    profile = Profile.query.order_by(Profile.id.asc()).first()
    skills = Skill.query.order_by(Skill.sort_order.asc(), Skill.id.asc()).all()
    experiences = Experience.query.order_by(Experience.sort_order.asc(), Experience.id.asc()).all()
    projects = Project.query.filter_by(is_featured=True).order_by(Project.sort_order.asc(), Project.id.asc()).all()
    return render_template(
        "public/home.html",
        profile=profile,
        skills=skills,
        experiences=experiences,
        projects=projects,
    )


@public_bp.post("/contact")
def contact():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    subject = request.form.get("subject", "").strip()
    message = request.form.get("message", "").strip()

    if not all([name, email, subject, message]):
        flash("Semua kolom kontak wajib diisi.", "danger")
        return redirect(url_for("public.home") + "#contact")

    if parseaddr(email)[1] != email or "@" not in email:
        flash("Format email belum valid.", "danger")
        return redirect(url_for("public.home") + "#contact")

    if len(name) > 150 or len(email) > 190 or len(subject) > 220 or len(message) > 5000:
        flash("Isi formulir terlalu panjang.", "danger")
        return redirect(url_for("public.home") + "#contact")

    contact_message = ContactMessage(name=name, email=email, subject=subject, message=message)
    db.session.add(contact_message)
    db.session.commit()

    try:
        send_contact_notification(contact_message)
        flash("Pesan berhasil dikirim. Terima kasih sudah menghubungi saya.", "success")
    except Exception:
        current_app.logger.exception("Gagal mengirim notifikasi Resend")
        flash("Pesan tersimpan, tetapi notifikasi email belum terkirim. Periksa konfigurasi Resend.", "warning")

    return redirect(url_for("public.home") + "#contact")
