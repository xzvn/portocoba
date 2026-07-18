from pathlib import Path

import cloudinary
import cloudinary.uploader
from flask import current_app

ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
ALLOWED_CV_EXTENSIONS = {".pdf"}


def _configure():
    cloud_name = current_app.config["CLOUDINARY_CLOUD_NAME"]
    api_key = current_app.config["CLOUDINARY_API_KEY"]
    api_secret = current_app.config["CLOUDINARY_API_SECRET"]
    if not all([cloud_name, api_key, api_secret]):
        raise RuntimeError("Konfigurasi Cloudinary belum lengkap.")

    cloudinary.config(
        cloud_name=cloud_name,
        api_key=api_key,
        api_secret=api_secret,
        secure=True,
    )


def upload_image(file_storage, folder="portfolio/images"):
    if not file_storage or not file_storage.filename:
        return None
    suffix = Path(file_storage.filename).suffix.lower()
    if suffix not in ALLOWED_IMAGE_EXTENSIONS:
        raise ValueError("Format gambar harus JPG, JPEG, PNG, WEBP, atau GIF.")

    _configure()
    result = cloudinary.uploader.upload(
        file_storage,
        folder=folder,
        resource_type="image",
        overwrite=False,
        unique_filename=True,
    )
    return {"url": result["secure_url"], "public_id": result["public_id"]}


def upload_cv(file_storage, folder="portfolio/cv"):
    if not file_storage or not file_storage.filename:
        return None
    suffix = Path(file_storage.filename).suffix.lower()
    if suffix not in ALLOWED_CV_EXTENSIONS:
        raise ValueError("CV harus menggunakan format PDF.")

    _configure()
    result = cloudinary.uploader.upload(
        file_storage,
        folder=folder,
        resource_type="raw",
        overwrite=False,
        unique_filename=True,
        use_filename=True,
    )
    return {"url": result["secure_url"], "public_id": result["public_id"]}
