from datetime import datetime
from flask_login import UserMixin
from app.extensions import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(30), default='member')
    balance = db.Column(db.Float, default=0)
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

class Banner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    subtitle = db.Column(db.Text, default='')
    image_url = db.Column(db.String(255), default='')
    button_text = db.Column(db.String(50), default='Lihat Promo')
    button_url = db.Column(db.String(255), default='/promosi')
    is_active = db.Column(db.Boolean, default=True)

class Promotion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, default='')
    badge = db.Column(db.String(50), default='PROMO')
    is_active = db.Column(db.Boolean, default=True)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    trx_type = db.Column(db.String(30), nullable=False)
    amount = db.Column(db.Float, default=0)
    status = db.Column(db.String(30), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Setting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text, default='')
