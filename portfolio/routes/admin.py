from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user
from sqlalchemy import func

from ..extensions import db
from ..models import ContactMessage, Experience, Profile, Project, Skill
from ..services.cloudinary_service import upload_cv, upload_image

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.before_request
def protect_admin():
    if not current_user.is_authenticated:
        return redirect(url_for("auth.login"))


def _to_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


@admin_bp.get("/")
def dashboard():
    counts = {
        "skills": db.session.scalar(db.select(func.count(Skill.id))) or 0,
        "experiences": db.session.scalar(db.select(func.count(Experience.id))) or 0,
        "projects": db.session.scalar(db.select(func.count(Project.id))) or 0,
        "messages": db.session.scalar(db.select(func.count(ContactMessage.id))) or 0,
        "unread": db.session.scalar(db.select(func.count(ContactMessage.id)).where(ContactMessage.is_read.is_(False))) or 0,
    }
    recent_messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).limit(5).all()
    return render_template("admin/dashboard.html", counts=counts, recent_messages=recent_messages)


@admin_bp.route("/profile", methods=["GET", "POST"])
def profile():
    profile_data = Profile.query.order_by(Profile.id.asc()).first()
    if not profile_data:
        abort(500, "Jalankan scripts/init_db.py terlebih dahulu.")

    if request.method == "POST":
        text_fields = [
            "brand_name", "full_name", "headline", "short_intro", "availability_text",
            "about_text", "about_text_secondary", "years_experience", "email", "phone",
            "location", "education", "work_status", "github_url", "linkedin_url", "footer_text",
        ]
        for field in text_fields:
            value = request.form.get(field, "").strip()
            if field in {"github_url", "linkedin_url"}:
                value = value or None
            setattr(profile_data, field, value)

        try:
            hero_upload = upload_image(request.files.get("hero_image"), "portfolio/profile")
            if hero_upload:
                profile_data.hero_image_url = hero_upload["url"]
                profile_data.hero_image_public_id = hero_upload["public_id"]

            about_upload = upload_image(request.files.get("about_image"), "portfolio/profile")
            if about_upload:
                profile_data.about_image_url = about_upload["url"]
                profile_data.about_image_public_id = about_upload["public_id"]

            cv_upload = upload_cv(request.files.get("cv_file"), "portfolio/cv")
            if cv_upload:
                profile_data.cv_url = cv_upload["url"]
                profile_data.cv_public_id = cv_upload["public_id"]
        except (RuntimeError, ValueError) as error:
            flash(str(error), "danger")
            return render_template("admin/profile.html", profile=profile_data)

        db.session.commit()
        flash("Profil berhasil diperbarui.", "success")
        return redirect(url_for("admin.profile"))

    return render_template("admin/profile.html", profile=profile_data)


@admin_bp.get("/skills")
def skills():
    data = Skill.query.order_by(Skill.sort_order.asc(), Skill.id.asc()).all()
    return render_template("admin/skills.html", skills=data)


@admin_bp.route("/skills/new", methods=["GET", "POST"])
@admin_bp.route("/skills/<int:item_id>/edit", methods=["GET", "POST"])
def skill_form(item_id=None):
    item = db.session.get(Skill, item_id) if item_id else Skill()
    if item_id and not item:
        abort(404)

    if request.method == "POST":
        item.category = request.form.get("category", "").strip()
        item.icon = request.form.get("icon", "code").strip() or "code"
        item.items = request.form.get("items", "").strip()
        item.sort_order = _to_int(request.form.get("sort_order"))
        if not item.category or not item.items:
            flash("Kategori dan daftar kemampuan wajib diisi.", "danger")
            return render_template("admin/skill_form.html", item=item)
        db.session.add(item)
        db.session.commit()
        flash("Data skill berhasil disimpan.", "success")
        return redirect(url_for("admin.skills"))
    return render_template("admin/skill_form.html", item=item)


@admin_bp.post("/skills/<int:item_id>/delete")
def skill_delete(item_id):
    item = db.session.get(Skill, item_id) or abort(404)
    db.session.delete(item)
    db.session.commit()
    flash("Skill berhasil dihapus.", "success")
    return redirect(url_for("admin.skills"))


@admin_bp.get("/experiences")
def experiences():
    data = Experience.query.order_by(Experience.sort_order.asc(), Experience.id.asc()).all()
    return render_template("admin/experiences.html", experiences=data)


@admin_bp.route("/experiences/new", methods=["GET", "POST"])
@admin_bp.route("/experiences/<int:item_id>/edit", methods=["GET", "POST"])
def experience_form(item_id=None):
    item = db.session.get(Experience, item_id) if item_id else Experience()
    if item_id and not item:
        abort(404)

    if request.method == "POST":
        item.period = request.form.get("period", "").strip()
        item.title = request.form.get("title", "").strip()
        item.organization = request.form.get("organization", "").strip()
        item.description = request.form.get("description", "").strip()
        item.item_type = request.form.get("item_type", "experience")
        item.sort_order = _to_int(request.form.get("sort_order"))
        item.is_active = request.form.get("is_active") == "on"
        if not all([item.period, item.title, item.organization, item.description]):
            flash("Semua kolom utama wajib diisi.", "danger")
            return render_template("admin/experience_form.html", item=item)
        db.session.add(item)
        db.session.commit()
        flash("Pengalaman atau pendidikan berhasil disimpan.", "success")
        return redirect(url_for("admin.experiences"))
    return render_template("admin/experience_form.html", item=item)


@admin_bp.post("/experiences/<int:item_id>/delete")
def experience_delete(item_id):
    item = db.session.get(Experience, item_id) or abort(404)
    db.session.delete(item)
    db.session.commit()
    flash("Data berhasil dihapus.", "success")
    return redirect(url_for("admin.experiences"))


@admin_bp.get("/projects")
def projects():
    data = Project.query.order_by(Project.sort_order.asc(), Project.id.asc()).all()
    return render_template("admin/projects.html", projects=data)


@admin_bp.route("/projects/new", methods=["GET", "POST"])
@admin_bp.route("/projects/<int:item_id>/edit", methods=["GET", "POST"])
def project_form(item_id=None):
    item = db.session.get(Project, item_id) if item_id else Project()
    if item_id and not item:
        abort(404)

    if request.method == "POST":
        item.title = request.form.get("title", "").strip()
        item.description = request.form.get("description", "").strip()
        item.technologies = request.form.get("technologies", "").strip()
        item.live_url = request.form.get("live_url", "").strip() or None
        item.code_url = request.form.get("code_url", "").strip() or None
        item.sort_order = _to_int(request.form.get("sort_order"))
        item.is_featured = request.form.get("is_featured") == "on"

        try:
            image_upload = upload_image(request.files.get("image"), "portfolio/projects")
            if image_upload:
                item.image_url = image_upload["url"]
                item.image_public_id = image_upload["public_id"]
        except (RuntimeError, ValueError) as error:
            flash(str(error), "danger")
            return render_template("admin/project_form.html", item=item)

        if not all([item.title, item.description, item.technologies]):
            flash("Judul, deskripsi, dan teknologi wajib diisi.", "danger")
            return render_template("admin/project_form.html", item=item)

        db.session.add(item)
        db.session.commit()
        flash("Proyek berhasil disimpan.", "success")
        return redirect(url_for("admin.projects"))
    return render_template("admin/project_form.html", item=item)


@admin_bp.post("/projects/<int:item_id>/delete")
def project_delete(item_id):
    item = db.session.get(Project, item_id) or abort(404)
    db.session.delete(item)
    db.session.commit()
    flash("Proyek berhasil dihapus.", "success")
    return redirect(url_for("admin.projects"))


@admin_bp.get("/messages")
def messages():
    data = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return render_template("admin/messages.html", messages=data)


@admin_bp.get("/messages/<int:item_id>")
def message_detail(item_id):
    item = db.session.get(ContactMessage, item_id) or abort(404)
    if not item.is_read:
        item.is_read = True
        db.session.commit()
    return render_template("admin/message_detail.html", item=item)


@admin_bp.post("/messages/<int:item_id>/delete")
def message_delete(item_id):
    item = db.session.get(ContactMessage, item_id) or abort(404)
    db.session.delete(item)
    db.session.commit()
    flash("Pesan berhasil dihapus.", "success")
    return redirect(url_for("admin.messages"))
