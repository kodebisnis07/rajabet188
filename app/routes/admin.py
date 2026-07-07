from datetime import datetime
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from app.extensions import db
from app.models import (User, Provider, Game, Banner, Promotion, Transaction, Setting,
                        PaymentGateway, MediaFile, SeoSetting, ThemeSetting, PageSection,
                        AuditLog, Role)
from app.services.audit import log_action

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


def bool_field(name):
    return bool(request.form.get(name))


@admin_bp.route('/')
@admin_required
def dashboard():
    deposits = Transaction.query.filter_by(trx_type='deposit')
    withdraws = Transaction.query.filter_by(trx_type='withdraw')
    stats={
        'members': User.query.filter_by(role='member').count(),
        'providers': Provider.query.count(),
        'games': Game.query.count(),
        'promos': Promotion.query.count(),
        'pending_deposit': deposits.filter_by(status='pending').count(),
        'pending_withdraw': withdraws.filter_by(status='pending').count(),
        'deposit_success': round(sum(t.amount for t in Transaction.query.filter_by(trx_type='deposit', status='success').all()), 2),
        'withdraw_success': round(sum(t.amount for t in Transaction.query.filter_by(trx_type='withdraw', status='success').all()), 2),
    }
    logs = AuditLog.query.order_by(AuditLog.created_at.desc()).limit(8).all()
    return render_template('admin/dashboard.html', stats=stats, logs=logs)


@admin_bp.route('/providers', methods=['GET','POST'])
@admin_required
def providers():
    if request.method=='POST':
        p = Provider(name=request.form['name'], category=request.form['category'], icon=request.form.get('icon','🎮'), logo_url=request.form.get('logo_url',''), sort_order=int(request.form.get('sort_order',0)), is_active=bool_field('is_active'))
        db.session.add(p); db.session.commit(); log_action('provider.create', p.name)
        flash('Provider ditambahkan.', 'success'); return redirect(url_for('admin.providers'))
    return render_template('admin/providers.html', providers=Provider.query.order_by(Provider.sort_order.asc()).all())


@admin_bp.route('/providers/<int:item_id>/toggle')
@admin_required
def toggle_provider(item_id):
    p = Provider.query.get_or_404(item_id); p.is_active = not p.is_active; db.session.commit(); log_action('provider.toggle', p.name)
    return redirect(url_for('admin.providers'))


@admin_bp.route('/providers/<int:item_id>/delete')
@admin_required
def delete_provider(item_id):
    p = Provider.query.get_or_404(item_id); db.session.delete(p); db.session.commit(); log_action('provider.delete', p.name)
    return redirect(url_for('admin.providers'))


@admin_bp.route('/games', methods=['GET','POST'])
@admin_required
def games():
    if request.method=='POST':
        g = Game(name=request.form['name'], category=request.form['category'], provider_name=request.form.get('provider_name','Rajabet188'), thumbnail=request.form.get('thumbnail',''), rtp=int(request.form.get('rtp',96)), status=request.form.get('status','active'), is_hot=bool_field('is_hot'), is_new=bool_field('is_new'), is_maintenance=bool_field('is_maintenance'))
        db.session.add(g); db.session.commit(); log_action('game.create', g.name)
        flash('Game ditambahkan.', 'success'); return redirect(url_for('admin.games'))
    return render_template('admin/games.html', games=Game.query.order_by(Game.created_at.desc()).all(), providers=Provider.query.all())


@admin_bp.route('/games/<int:item_id>/delete')
@admin_required
def delete_game(item_id):
    g = Game.query.get_or_404(item_id); db.session.delete(g); db.session.commit(); log_action('game.delete', g.name)
    return redirect(url_for('admin.games'))


@admin_bp.route('/banners', methods=['GET','POST'])
@admin_required
def banners():
    if request.method=='POST':
        b = Banner(title=request.form['title'], subtitle=request.form.get('subtitle',''), image_url=request.form.get('image_url',''), button_text=request.form.get('button_text','Daftar'), button_url=request.form.get('button_url','/register'), placement=request.form.get('placement','homepage'), sort_order=int(request.form.get('sort_order',0)), is_active=bool_field('is_active'))
        db.session.add(b); db.session.commit(); log_action('banner.create', b.title)
        flash('Banner ditambahkan.', 'success'); return redirect(url_for('admin.banners'))
    return render_template('admin/banners.html', banners=Banner.query.order_by(Banner.sort_order.asc()).all())


@admin_bp.route('/banners/<int:item_id>/delete')
@admin_required
def delete_banner(item_id):
    b = Banner.query.get_or_404(item_id); db.session.delete(b); db.session.commit(); log_action('banner.delete', b.title)
    return redirect(url_for('admin.banners'))


@admin_bp.route('/promos', methods=['GET','POST'])
@admin_required
def promos():
    if request.method=='POST':
        p = Promotion(title=request.form['title'], description=request.form.get('description',''), badge=request.form.get('badge','PROMO'), image_url=request.form.get('image_url',''), start_at=request.form.get('start_at',''), end_at=request.form.get('end_at',''), is_active=bool_field('is_active'))
        db.session.add(p); db.session.commit(); log_action('promo.create', p.title)
        flash('Promo ditambahkan.', 'success'); return redirect(url_for('admin.promos'))
    return render_template('admin/promos.html', promos=Promotion.query.order_by(Promotion.created_at.desc()).all())


@admin_bp.route('/promos/<int:item_id>/delete')
@admin_required
def delete_promo(item_id):
    p = Promotion.query.get_or_404(item_id); db.session.delete(p); db.session.commit(); log_action('promo.delete', p.title)
    return redirect(url_for('admin.promos'))


@admin_bp.route('/members', methods=['GET','POST'])
@admin_required
def members():
    if request.method=='POST':
        m = User.query.get_or_404(int(request.form['member_id']))
        m.balance = float(request.form.get('balance', m.balance))
        m.vip_level = request.form.get('vip_level', m.vip_level)
        m.is_active = bool_field('is_active')
        db.session.commit(); log_action('member.update', m.username)
        flash('Member diperbarui.', 'success'); return redirect(url_for('admin.members'))
    return render_template('admin/members.html', members=User.query.order_by(User.created_at.desc()).all())


@admin_bp.route('/transactions', methods=['GET','POST'])
@admin_required
def transactions():
    if request.method=='POST':
        trx = Transaction(user_id=request.form.get('user_id') or None, trx_type=request.form['trx_type'], amount=float(request.form.get('amount',0)), method=request.form.get('method','Manual'), note=request.form.get('note',''), status=request.form.get('status','pending'))
        db.session.add(trx); db.session.commit(); log_action('transaction.create', f'{trx.trx_type} {trx.amount}')
        flash('Transaksi ditambahkan.', 'success'); return redirect(url_for('admin.transactions'))
    data = Transaction.query.order_by(Transaction.created_at.desc()).all()
    return render_template('admin/transactions.html', transactions=data, members=User.query.all())


@admin_bp.route('/transactions/<int:item_id>/<status>')
@admin_required
def transaction_status(item_id, status):
    trx = Transaction.query.get_or_404(item_id)
    if status in ['pending','success','failed','rejected']:
        trx.status = status; trx.processed_at = datetime.utcnow(); db.session.commit(); log_action('transaction.status', f'{item_id} -> {status}')
    return redirect(url_for('admin.transactions'))


@admin_bp.route('/payments', methods=['GET','POST'])
@admin_required
def payments():
    if request.method=='POST':
        pg = PaymentGateway(name=request.form['name'], code=request.form['code'], mode=request.form.get('mode','manual'), config_json=request.form.get('config_json','{}'), is_active=bool_field('is_active'))
        db.session.add(pg); db.session.commit(); log_action('payment.create', pg.name)
        return redirect(url_for('admin.payments'))
    return render_template('admin/payments.html', gateways=PaymentGateway.query.all())


@admin_bp.route('/media', methods=['GET','POST'])
@admin_required
def media():
    if request.method=='POST':
        m = MediaFile(title=request.form['title'], file_url=request.form['file_url'], media_type=request.form.get('media_type','image'))
        db.session.add(m); db.session.commit(); log_action('media.create', m.title)
        return redirect(url_for('admin.media'))
    return render_template('admin/media.html', media_files=MediaFile.query.order_by(MediaFile.created_at.desc()).all())


@admin_bp.route('/seo', methods=['GET','POST'])
@admin_required
def seo():
    if request.method=='POST':
        page = request.form['page']
        item = SeoSetting.query.filter_by(page=page).first() or SeoSetting(page=page)
        item.meta_title = request.form.get('meta_title','')
        item.meta_description = request.form.get('meta_description','')
        item.og_image = request.form.get('og_image','')
        db.session.add(item); db.session.commit(); log_action('seo.save', page)
        return redirect(url_for('admin.seo'))
    return render_template('admin/seo.html', seo_items=SeoSetting.query.all())


@admin_bp.route('/theme', methods=['GET','POST'])
@admin_required
def theme():
    theme = ThemeSetting.query.filter_by(is_active=True).first() or ThemeSetting()
    if request.method=='POST':
        theme.name = request.form.get('name','Dark Gold')
        theme.primary_color = request.form.get('primary_color','#f6c85f')
        theme.background_color = request.form.get('background_color','#070707')
        theme.accent_color = request.form.get('accent_color','#9e650d')
        db.session.add(theme); db.session.commit(); log_action('theme.save', theme.name)
        return redirect(url_for('admin.theme'))
    return render_template('admin/theme.html', theme=theme)


@admin_bp.route('/builder', methods=['GET','POST'])
@admin_required
def builder():
    if request.method=='POST':
        section = PageSection(section_key=request.form['section_key'], title=request.form.get('title',''), content=request.form.get('content',''), sort_order=int(request.form.get('sort_order',0)), is_active=bool_field('is_active'))
        db.session.add(section); db.session.commit(); log_action('builder.section.create', section.section_key)
        return redirect(url_for('admin.builder'))
    return render_template('admin/builder.html', sections=PageSection.query.order_by(PageSection.sort_order.asc()).all())


@admin_bp.route('/roles', methods=['GET','POST'])
@admin_required
def roles():
    if request.method=='POST':
        r = Role(name=request.form['name'], description=request.form.get('description',''), permissions=request.form.get('permissions',''))
        db.session.add(r); db.session.commit(); log_action('role.create', r.name)
        return redirect(url_for('admin.roles'))
    return render_template('admin/roles.html', roles=Role.query.all())


@admin_bp.route('/audit-log')
@admin_required
def audit_log():
    return render_template('admin/audit_log.html', logs=AuditLog.query.order_by(AuditLog.created_at.desc()).limit(200).all())


@admin_bp.route('/settings', methods=['GET','POST'])
@admin_required
def settings():
    if request.method=='POST':
        for k,v in request.form.items():
            s=Setting.query.filter_by(key=k).first() or Setting(key=k)
            s.value=v
            db.session.add(s)
        db.session.commit(); log_action('settings.save', 'website settings')
        flash('Pengaturan disimpan.', 'success'); return redirect(url_for('admin.settings'))
    settings={s.key:s.value for s in Setting.query.all()}
    return render_template('admin/settings.html', settings=settings)
