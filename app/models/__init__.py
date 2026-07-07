from datetime import datetime
from flask_login import UserMixin
from app.extensions import db

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255), default='')
    permissions = db.Column(db.Text, default='')

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(30), default='member')
    balance = db.Column(db.Float, default=0)
    vip_level = db.Column(db.String(30), default='Bronze')
    referral_code = db.Column(db.String(50), default='')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Provider(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    icon = db.Column(db.String(10), default='🎮')
    logo_url = db.Column(db.String(255), default='')
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    provider_name = db.Column(db.String(120), default='Rajabet188')
    thumbnail = db.Column(db.String(255), default='')
    rtp = db.Column(db.Integer, default=96)
    status = db.Column(db.String(30), default='active')
    is_hot = db.Column(db.Boolean, default=False)
    is_new = db.Column(db.Boolean, default=False)
    is_maintenance = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Banner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    subtitle = db.Column(db.Text, default='')
    image_url = db.Column(db.String(255), default='')
    button_text = db.Column(db.String(50), default='Lihat Promo')
    button_url = db.Column(db.String(255), default='/promosi')
    placement = db.Column(db.String(50), default='homepage')
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Promotion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, default='')
    badge = db.Column(db.String(50), default='PROMO')
    image_url = db.Column(db.String(255), default='')
    start_at = db.Column(db.String(40), default='')
    end_at = db.Column(db.String(40), default='')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    trx_type = db.Column(db.String(30), nullable=False)  # deposit / withdraw / bonus
    amount = db.Column(db.Float, default=0)
    method = db.Column(db.String(80), default='Manual')
    note = db.Column(db.Text, default='')
    status = db.Column(db.String(30), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    processed_at = db.Column(db.DateTime, nullable=True)

class PaymentGateway(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(50), unique=True, nullable=False)
    mode = db.Column(db.String(30), default='manual')
    config_json = db.Column(db.Text, default='{}')
    is_active = db.Column(db.Boolean, default=False)

class MediaFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    file_url = db.Column(db.String(255), nullable=False)
    media_type = db.Column(db.String(50), default='image')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SeoSetting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page = db.Column(db.String(100), unique=True, nullable=False)
    meta_title = db.Column(db.String(180), default='')
    meta_description = db.Column(db.Text, default='')
    og_image = db.Column(db.String(255), default='')

class ThemeSetting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), default='Dark Gold')
    primary_color = db.Column(db.String(20), default='#f6c85f')
    background_color = db.Column(db.String(20), default='#070707')
    accent_color = db.Column(db.String(20), default='#9e650d')
    is_active = db.Column(db.Boolean, default=True)

class PageSection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    section_key = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(150), default='')
    content = db.Column(db.Text, default='')
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)

class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, nullable=True)
    action = db.Column(db.String(150), nullable=False)
    detail = db.Column(db.Text, default='')
    ip_address = db.Column(db.String(80), default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Setting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text, default='')
