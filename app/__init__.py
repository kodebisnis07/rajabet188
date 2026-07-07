from flask import Flask
from .extensions import db, migrate, login_manager


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .routes.home import home_bp
    from .routes.auth import auth_bp
    from .routes.admin import admin_bp
    from .routes.pages import pages_bp
    from .api.routes import api_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(pages_bp)
    app.register_blueprint(api_bp, url_prefix='/api')

    with app.app_context():
        db.create_all()
        seed_defaults()

    return app


def seed_defaults():
    from .models import (User, Provider, Game, Banner, Promotion, Setting, Role,
                         PaymentGateway, SeoSetting, ThemeSetting, PageSection)
    from werkzeug.security import generate_password_hash

    for role, desc in [
        ('superadmin','Akses penuh'),('admin','Kelola konten'),('cs','Customer support'),
        ('finance','Deposit dan withdraw'),('member','Member website')]:
        if not Role.query.filter_by(name=role).first():
            db.session.add(Role(name=role, description=desc, permissions='all' if role=='superadmin' else role))

    if not User.query.filter_by(username='admin').first():
        db.session.add(User(username='admin', email='admin@rajabet188.local', password_hash=generate_password_hash('admin123'), role='superadmin', referral_code='ADMIN188'))

    defaults = {
        'site_name':'Rajabet188',
        'running_text':'Selamat datang di Rajabet188 - promo, event VIP, dan hiburan premium setiap hari.',
        'whatsapp':'', 'telegram':'', 'maintenance_mode':'off'
    }
    for key, value in defaults.items():
        if not Setting.query.filter_by(key=key).first():
            db.session.add(Setting(key=key, value=value))

    if ThemeSetting.query.count() == 0:
        db.session.add(ThemeSetting(name='Dark Gold', primary_color='#f6c85f', background_color='#070707', accent_color='#9e650d', is_active=True))

    if SeoSetting.query.count() == 0:
        db.session.add(SeoSetting(page='home', meta_title='Rajabet188 - Premium Dark Gold Entertainment', meta_description='Rajabet188 hadir dengan tampilan premium, mobile friendly, dan panel admin modern.'))

    if Provider.query.count() == 0:
        providers=[('Slot','PG Soft','🔥'),('Live Casino','Evolution','🎲'),('Sportsbook','SBO Sports','⚽'),('Togel','Rajabet Pools','🎯'),('Fishing','JILI Fishing','🐟'),('Arcade','Arcade Arena','🕹️'),('Crash','Crash X','🚀'),('Poker','Poker Club','♠️')]
        for i,(cat,name,icon) in enumerate(providers):
            db.session.add(Provider(name=name, category=cat, icon=icon, is_active=True, sort_order=i))


    for i, (cat, name, icon) in enumerate([('Slot','Pragmatic Play','🎰'), ('Slot','PG Soft','🀄')], start=20):
        if not Provider.query.filter_by(name=name).first():
            db.session.add(Provider(name=name, category=cat, icon=icon, is_active=True, sort_order=i))

    # Seed / sync game list from the uploaded reference, using original Rajabet188 assets generated in this project.
    demo_slot_games = [
        ('Power Of Ninja', 'Slot', 'Pragmatic Play', '/static/img/games/power-of-ninja.svg', 'Gacor'),
        ('Starlight Princess', 'Slot', 'Pragmatic Play', '/static/img/games/starlight-princess.svg', 'Maxwin'),
        ('Aztec Gems', 'Slot', 'Pragmatic Play', '/static/img/games/aztec-gems.svg', 'Gacor'),
        ('Plinko', 'Slot', 'Pragmatic Play', '/static/img/games/plinko.svg', 'X16 Maxwin'),
        ('Starlight Princess 1000', 'Slot', 'Pragmatic Play', '/static/img/games/starlight-princess-1000.svg', 'x1000'),
        ('Bonanza Gold', 'Slot', 'Pragmatic Play', '/static/img/games/bonanza-gold.svg', 'Gacor'),
        ('Mahjong Wins Bonus', 'Slot', 'Pragmatic Play', '/static/img/games/mahjong-wins-bonus.svg', 'Scatter Hitam'),
        ('Gates Of Olympus Dice', 'Slot', 'Pragmatic Play', '/static/img/games/gates-of-olympus-dice.svg', 'Dice'),
        ('Gates Of Gatot Kaca', 'Slot', 'Pragmatic Play', '/static/img/games/gates-of-gatot-kaca.svg', 'Maxwin'),
        ('Gates Of Olympus 1000', 'Slot', 'Pragmatic Play', '/static/img/games/gates-of-olympus-1000.svg', 'x1000'),
        ('Pyramid Bonanza', 'Slot', 'Pragmatic Play', '/static/img/games/pyramid-bonanza.svg', 'Gacor'),
        ('Wild West Gold', 'Slot', 'Pragmatic Play', '/static/img/games/wild-west-gold.svg', 'Gacor'),
        ('Twilight Princess', 'Slot', 'Pragmatic Play', '/static/img/games/twilight-princess.svg', 'Super Scatter'),
        ('Sugar Rush', 'Slot', 'Pragmatic Play', '/static/img/games/sugar-rush.svg', 'Maxwin'),
        ('Jasmine Dreams', 'Slot', 'Pragmatic Play', '/static/img/games/jasmine-dreams.svg', 'Gacor'),
        ('Mahjong Panda', 'Slot', 'Pragmatic Play', '/static/img/games/mahjong-panda.svg', 'Gacor'),
        ('Gates Of Olympus', 'Slot', 'Pragmatic Play', '/static/img/games/gates-of-olympus.svg', 'Maxwin'),
        ('Starlight Princess Xmas', 'Slot', 'Pragmatic Play', '/static/img/games/starlight-princess-xmas.svg', 'Gacor'),
        ('Big Bass Bonanza', 'Slot', 'Pragmatic Play', '/static/img/games/big-bass-bonanza.svg', 'Gacor'),
        ('Gates Of Gatotkaca 1000', 'Slot', 'Pragmatic Play', '/static/img/games/gates-of-gatotkaca-1000.svg', 'x1000'),
        ('Sweet Bonanza', 'Slot', 'Pragmatic Play', '/static/img/games/sweet-bonanza.svg', 'Maxwin'),
        ('Mochimon', 'Slot', 'Pragmatic Play', '/static/img/games/mochimon.svg', 'Gacor'),
        ('Rujak Bonanza', 'Slot', 'Pragmatic Play', '/static/img/games/rujak-bonanza.svg', 'Gacor'),
        ('Wisdom Of Athena', 'Slot', 'Pragmatic Play', '/static/img/games/wisdom-of-athena.svg', 'Gacor'),
        ('Lucky Neko', 'Slot', 'PG Soft', '/static/img/games/lucky-neko.svg', 'Gacor'),
        ('Jurassic Kingdom', 'Slot', 'PG Soft', '/static/img/games/jurassic-kingdom.svg', 'Gacor'),
        ('Mahjong Ways', 'Slot', 'PG Soft', '/static/img/games/mahjong-ways.svg', 'Maxwin'),
        ('Dragon Hatch', 'Slot', 'PG Soft', '/static/img/games/dragon-hatch.svg', 'Gacor'),
        ('Wild Bandito', 'Slot', 'PG Soft', '/static/img/games/wild-bandito.svg', 'Gacor'),
        ('Songkran Splash', 'Slot', 'PG Soft', '/static/img/games/songkran-splash.svg', 'Gacor'),
        ('Piggy Gold', 'Slot', 'PG Soft', '/static/img/games/piggy-gold.svg', 'Gacor'),
        ('Queen Bounty', 'Slot', 'PG Soft', '/static/img/games/queen-bounty.svg', 'Gacor'),
        ('Caishen Wins', 'Slot', 'PG Soft', '/static/img/games/caishen-wins.svg', 'Gacor'),
        ('Mahjong Ways 2', 'Slot', 'PG Soft', '/static/img/games/mahjong-ways-2.svg', 'Maxwin'),
        ('The Great Escape', 'Slot', 'PG Soft', '/static/img/games/the-great-escape.svg', 'Gacor'),
        ('Leprechaun Riches', 'Slot', 'PG Soft', '/static/img/games/leprechaun-riches.svg', 'Gacor'),
        ('Dream Of Macau', 'Slot', 'PG Soft', '/static/img/games/dream-of-macau.svg', 'Gacor'),
        ('Spirited Wonders', 'Slot', 'PG Soft', '/static/img/games/spirited-wonders.svg', 'Gacor'),
        ('Ganesha Gold', 'Slot', 'PG Soft', '/static/img/games/ganesha-gold.svg', 'Gacor')
    ]
    for idx, (name, cat, provider, thumb, badge) in enumerate(demo_slot_games):
        existing = Game.query.filter_by(name=name, provider_name=provider).first()
        if existing:
            existing.category = cat
            existing.thumbnail = thumb
            existing.status = 'active'
            existing.is_hot = idx < 12
            existing.is_new = provider == 'PG Soft'
        else:
            db.session.add(Game(
                name=name,
                category=cat,
                provider_name=provider,
                thumbnail=thumb,
                status='active',
                rtp=96 + (idx % 3),
                is_hot=idx < 12,
                is_new=provider == 'PG Soft'
            ))

    if Banner.query.count() == 0:
        db.session.add(Banner(title='Rajabet188 Premium', subtitle='Tema dark gold, mobile friendly, dan siap dikembangkan.', image_url='', button_text='Daftar Sekarang', button_url='/register', placement='homepage', is_active=True))

    if Promotion.query.count() == 0:
        db.session.add(Promotion(title='Bonus Member Baru', description='Promo spesial untuk member baru Rajabet188.', badge='NEW', is_active=True))
        db.session.add(Promotion(title='Cashback Mingguan', description='Cashback untuk member aktif setiap minggu.', badge='CASHBACK', is_active=True))

    if PaymentGateway.query.count() == 0:
        for name, code in [('Manual Transfer','manual'),('QRIS','qris'),('DANA','dana'),('OVO','ovo'),('GoPay','gopay'),('Bank Transfer','bank')]:
            db.session.add(PaymentGateway(name=name, code=code, mode='manual', is_active=(code=='manual')))

    if PageSection.query.count() == 0:
        db.session.add(PageSection(section_key='hero', title='Rajabet188', content='Platform hiburan premium dengan tampilan modern.', sort_order=1))
        db.session.add(PageSection(section_key='features', title='Fitur Unggulan', content='Mobile first, admin panel, banner, provider, game, promo, dan member manager.', sort_order=2))

    db.session.commit()
