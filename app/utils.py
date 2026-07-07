import os
import re
from datetime import datetime
from werkzeug.utils import secure_filename
from app.extensions import db

ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "gif"}


def slugify(value):
    value = (value or "").strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or datetime.now().strftime("item-%Y%m%d%H%M%S")


def unique_slug(model, name, current_id=None):
    base = slugify(name)
    slug = base
    counter = 2
    while True:
        query = model.query.filter_by(slug=slug)
        if current_id:
            query = query.filter(model.id != current_id)
        if not query.first():
            return slug
        slug = f"{base}-{counter}"
        counter += 1


def allowed_image(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS


def save_uploaded_image(file, folder):
    if not file or not file.filename:
        return None
    if not allowed_image(file.filename):
        raise ValueError("Format gambar harus png, jpg, jpeg, webp, atau gif")

    os.makedirs(folder, exist_ok=True)
    filename = secure_filename(file.filename)
    name, ext = os.path.splitext(filename)
    final_name = f"{slugify(name)}-{datetime.now().strftime('%Y%m%d%H%M%S%f')}{ext.lower()}"
    file.save(os.path.join(folder, final_name))
    return final_name


def get_setting(key, default=None):
    from app.models import Setting
    setting = Setting.query.filter_by(key=key).first()
    return setting.value if setting and setting.value not in (None, "") else default


def set_setting(key, value):
    from app.models import Setting
    setting = Setting.query.filter_by(key=key).first()
    if not setting:
        setting = Setting(key=key)
        db.session.add(setting)
    setting.value = value
    return setting
