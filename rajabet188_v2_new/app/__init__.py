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

    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(pages_bp)

    with app.app_context():
        db.create_all()
        seed_defaults()

    return app

def seed_defaults():
    from .models import User, Provider, Game, Banner, Promotion, Setting
    from werkzeug.security import generate_password_hash
    if not User.query.filter_by(username='admin').first():
        db.session.add(User(username='admin', email='admin@rajabet188.local', password_hash=generate_password_hash('admin123'), role='superadmin'))
    if not Setting.query.filter_by(key='site_name').first():
        db.session.add(Setting(key='site_name', value='Rajabet188'))
    if Provider.query.count() == 0:
        providers=[('Slot','PG Soft','🔥'),('Live Casino','Evolution','🎲'),('Sportsbook','SBO Sports','⚽'),('Togel','Rajabet Pools','🎯'),('Fishing','JILI Fishing','🐟'),('Arcade','Arcade Arena','🕹️')]
        for cat,name,icon in providers:
            db.session.add(Provider(name=name, category=cat, icon=icon, is_active=True))
    if Game.query.count() == 0:
        for name,cat in [('Mahjong Ways','Slot'),('Gates of Olympus','Slot'),('Sweet Bonanza','Slot'),('Baccarat Lobby','Live Casino'),('Roulette Royale','Live Casino'),('Liga Dunia','Sportsbook'),('Pasaran Nusantara','Togel'),('Ocean King','Fishing'),('Crash X','Arcade')]:
            db.session.add(Game(name=name, category=cat, provider_name='Rajabet188', thumbnail='', status='active', is_hot=True))
    if Banner.query.count() == 0:
        db.session.add(Banner(title='Selamat Datang di Rajabet188', subtitle='Platform hiburan premium dengan tampilan dark gold.', image_url='', button_text='Daftar Sekarang', button_url='/register', is_active=True))
    if Promotion.query.count() == 0:
        db.session.add(Promotion(title='Bonus Member Baru', description='Dapatkan promo spesial untuk akun baru Rajabet188.', badge='NEW', is_active=True))
    db.session.commit()
