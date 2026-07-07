from flask import Blueprint, render_template
from app.models import Game

pages_bp = Blueprint('pages', __name__)

CATEGORIES = {
    'slot': 'Slot',
    'live-casino': 'Live Casino',
    'sportsbook': 'Sportsbook',
    'togel': 'Togel',
    'arcade': 'Arcade',
    'fishing': 'Fishing',
}

@pages_bp.route('/<slug>')
def category_page(slug):
    if slug == 'promosi':
        return render_template('pages/promosi.html')
    if slug == 'vip':
        return render_template('pages/vip.html')
    category = CATEGORIES.get(slug)
    if not category:
        return render_template('errors/404.html'), 404
    games = Game.query.filter_by(category=category, status='active').all()
    return render_template('pages/category.html', category=category, games=games)
