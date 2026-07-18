from pathlib import Path

from flask import Flask, jsonify, send_from_directory
from werkzeug.middleware.proxy_fix import ProxyFix

from .config import Config
from .extensions import csrf, db, login_manager


def create_app(config_object=Config):
    package_dir = Path(__file__).resolve().parent
    template_dir = package_dir / "templates"

    app = Flask(
        __name__,
        static_folder=None,
        template_folder=str(template_dir),
    )

    app.config.from_object(config_object)

    app.wsgi_app = ProxyFix(
        app.wsgi_app,
        x_for=1,
        x_proto=1,
        x_host=1,
        x_port=1,
    )

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    login_manager.login_view = "auth.login"
    login_manager.login_message = "Silakan login untuk membuka halaman admin."
    login_manager.login_message_category = "warning"

    from .routes.admin import admin_bp
    from .routes.auth import auth_bp
    from .routes.public import public_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    public_dir = Path(app.root_path).parent / "public"

    @app.get("/css/<path:filename>")
    def public_css(filename):
        return send_from_directory(public_dir / "css", filename)

    @app.get("/js/<path:filename>")
    def public_js(filename):
        return send_from_directory(public_dir / "js", filename)

    @app.get("/images/<path:filename>")
    def public_images(filename):
        return send_from_directory(public_dir / "images", filename)

    @app.get("/health")
    def health():
        return jsonify({"status": "ok", "app": "minimalist-portfolio"})

    @app.errorhandler(404)
    def not_found(_error):
        return jsonify({"success": False, "message": "Halaman tidak ditemukan."}), 404

    @app.errorhandler(413)
    def file_too_large(_error):
        return jsonify({"success": False, "message": "Ukuran file terlalu besar. Maksimal 8 MB."}), 413

    return app
