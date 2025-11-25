from flask import Blueprint, jsonify
from app.models import User
from app import db

api = Blueprint('api', __name__)

# todo: make sure current_user is admin
@api.route('/toggle-user/<int:user_id>', methods=['POST'])
def toggle_user_status(user_id):
    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active
    db.session.commit()
    
    return jsonify({
        'success': True,
        'user_id': user_id,
        'is_active': user.is_active
    })

# todo: make sure current_user is admin
@api.route('/toggle-admin/<int:user_id>', methods=['POST'])
def toggle_admin_role(user_id):
    user = User.query.get_or_404(user_id)
    user.is_admin = not user.is_admin
    db.session.commit()
    
    return jsonify({
        'success': True,
        'user_id': user_id,
        'is_admin': user.is_admin
    })
