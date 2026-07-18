from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user

from ..models import User

auth_bp = Blueprint("auth", __name__, url_prefix="/admin")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("admin.dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        remember = request.form.get("remember") == "on"

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            flash("Email atau password salah.", "danger")
            return render_template("auth/login.html", email=email)

        login_user(user, remember=remember)
        flash("Login berhasil.", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("auth/login.html")


@auth_bp.post("/logout")
def logout():
    logout_user()
    flash("Anda sudah logout.", "success")
    return redirect(url_for("auth.login"))
