from flask import request
from flask_login import current_user
from app.extensions import db
from app.models import AuditLog

def log_action(action, detail=''):
    try:
        admin_id = current_user.id if getattr(current_user, 'is_authenticated', False) else None
        db.session.add(AuditLog(admin_id=admin_id, action=action, detail=detail, ip_address=request.remote_addr or ''))
        db.session.commit()
    except Exception:
        db.session.rollback()
