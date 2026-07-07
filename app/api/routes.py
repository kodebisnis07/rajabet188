from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models import Provider, Game, Banner, Promotion, Transaction, Setting

api_bp = Blueprint('api', __name__)

@api_bp.get('/health')
def health():
    return jsonify({'status':'ok','app':'Rajabet188'})

@api_bp.get('/home')
def home_data():
    return jsonify({
        'settings': {s.key: s.value for s in Setting.query.all()},
        'banners': [{'id':b.id,'title':b.title,'subtitle':b.subtitle,'button_url':b.button_url} for b in Banner.query.filter_by(is_active=True).all()],
        'providers': [{'id':p.id,'name':p.name,'category':p.category,'icon':p.icon} for p in Provider.query.filter_by(is_active=True).all()],
        'games': [{'id':g.id,'name':g.name,'category':g.category,'provider':g.provider_name,'rtp':g.rtp} for g in Game.query.filter_by(status='active').limit(20).all()],
        'promos': [{'id':p.id,'title':p.title,'badge':p.badge,'description':p.description} for p in Promotion.query.filter_by(is_active=True).all()]
    })

@api_bp.get('/games')
def games():
    category = request.args.get('category')
    q = Game.query.filter_by(status='active')
    if category:
        q = q.filter_by(category=category)
    return jsonify([{'id':g.id,'name':g.name,'category':g.category,'provider':g.provider_name,'rtp':g.rtp,'hot':g.is_hot,'new':g.is_new} for g in q.all()])

@api_bp.post('/transactions')
def create_transaction():
    data = request.get_json(silent=True) or {}
    trx = Transaction(user_id=data.get('user_id'), trx_type=data.get('trx_type','deposit'), amount=float(data.get('amount',0)), method=data.get('method','Manual'), note=data.get('note','API'), status='pending')
    db.session.add(trx); db.session.commit()
    return jsonify({'ok': True, 'transaction_id': trx.id, 'status': trx.status}), 201
