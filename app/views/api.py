from flask import Blueprint, jsonify
from app.models import User

api = Blueprint('api', __name__)

@api.route('/status')
def status():
    return jsonify({'status': 'ok'})

@api.route('/users')
def get_users():
    # Example endpoint
    return jsonify({'users': []})
