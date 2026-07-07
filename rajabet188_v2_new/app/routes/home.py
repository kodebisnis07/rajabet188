from flask import Blueprint, render_template
from app.models import Banner, Provider, Game, Promotion

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def index():
    banners = Banner.query.filter_by(is_active=True).all()
    providers = Provider.query.filter_by(is_active=True).order_by(Provider.sort_order.asc()).all()
    hot_games = Game.query.filter_by(status='active').limit(12).all()
    promos = Promotion.query.filter_by(is_active=True).all()
    return render_template('pages/index.html', banners=banners, providers=providers, hot_games=hot_games, promos=promos)
