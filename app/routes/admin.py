from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from app.extensions import db
from app.models import User, Provider, Game, Banner, Promotion, Transaction, Setting

admin_bp = Blueprint('admin', __name__)

def admin_required(fn):
    @wraps(fn)
    @login_required
    def wrapper(*args, **kwargs):
        if current_user.role not in ['superadmin','admin','cs','finance']:
            flash('Akses admin ditolak.', 'danger')
            return redirect(url_for('home.index'))
        return fn(*args, **kwargs)
    return wrapper

@admin_bp.route('/')
@admin_required
def dashboard():
    stats={
        'members': User.query.filter_by(role='member').count(),
        'providers': Provider.query.count(),
        'games': Game.query.count(),
        'promos': Promotion.query.count(),
        'pending_deposit': Transaction.query.filter_by(trx_type='deposit',status='pending').count(),
        'pending_withdraw': Transaction.query.filter_by(trx_type='withdraw',status='pending').count(),
    }
    return render_template('admin/dashboard.html', stats=stats)

@admin_bp.route('/providers', methods=['GET','POST'])
@admin_required
def providers():
    if request.method=='POST':
        db.session.add(Provider(name=request.form['name'], category=request.form['category'], icon=request.form.get('icon','🎮'), is_active=True))
        db.session.commit(); flash('Provider ditambahkan.', 'success'); return redirect(url_for('admin.providers'))
    return render_template('admin/providers.html', providers=Provider.query.all())

@admin_bp.route('/games', methods=['GET','POST'])
@admin_required
def games():
    if request.method=='POST':
        db.session.add(Game(name=request.form['name'], category=request.form['category'], provider_name=request.form.get('provider_name','Rajabet188'), rtp=int(request.form.get('rtp',96)), is_hot=bool(request.form.get('is_hot'))))
        db.session.commit(); flash('Game ditambahkan.', 'success'); return redirect(url_for('admin.games'))
    return render_template('admin/games.html', games=Game.query.all())

@admin_bp.route('/banners', methods=['GET','POST'])
@admin_required
def banners():
    if request.method=='POST':
        db.session.add(Banner(title=request.form['title'], subtitle=request.form.get('subtitle',''), button_text=request.form.get('button_text','Daftar'), button_url=request.form.get('button_url','/register'), is_active=True))
        db.session.commit(); flash('Banner ditambahkan.', 'success'); return redirect(url_for('admin.banners'))
    return render_template('admin/banners.html', banners=Banner.query.all())

@admin_bp.route('/promos', methods=['GET','POST'])
@admin_required
def promos():
    if request.method=='POST':
        db.session.add(Promotion(title=request.form['title'], description=request.form.get('description',''), badge=request.form.get('badge','PROMO'), is_active=True))
        db.session.commit(); flash('Promo ditambahkan.', 'success'); return redirect(url_for('admin.promos'))
    return render_template('admin/promos.html', promos=Promotion.query.all())

@admin_bp.route('/members')
@admin_required
def members():
    return render_template('admin/members.html', members=User.query.order_by(User.created_at.desc()).all())

@admin_bp.route('/settings', methods=['GET','POST'])
@admin_required
def settings():
    if request.method=='POST':
        for k,v in request.form.items():
            s=Setting.query.filter_by(key=k).first() or Setting(key=k)
            s.value=v
            db.session.add(s)
        db.session.commit(); flash('Pengaturan disimpan.', 'success'); return redirect(url_for('admin.settings'))
    settings={s.key:s.value for s in Setting.query.all()}
    return render_template('admin/settings.html', settings=settings)
