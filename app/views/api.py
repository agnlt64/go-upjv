from flask import Blueprint, request, redirect, url_for
from flask_login import login_user
from werkzeug.security import generate_password_hash, check_password_hash

from app.models import User
from app.utils import error, success
from app import db

api = Blueprint('api', __name__)

# todo: make sure current_user is admin
@api.route('/toggle-user/<int:user_id>', methods=['POST'])
def toggle_user_status(user_id):
    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active
    db.session.commit()
    
    return success('ok')

# todo: make sure current_user is admin
@api.route('/toggle-admin/<int:user_id>', methods=['POST'])
def toggle_admin_role(user_id):
    user = User.query.get_or_404(user_id)
    user.is_admin = not user.is_admin
    db.session.commit()
    
    return success('ok')

@api.route('/login', methods=['POST'])
def login():
    upjv_id = request.form.get('id_upjv')
    password = request.form.get('password')
    
    user = User.query.filter_by(upjv_id=upjv_id).first()
    if user:
        if check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main.user_profile'))
        else:
            return error('Invalid password')
    return error('User not found')

@api.route('/sign-up', methods=['POST'])
def sign_up():
    # todo: validate inputs
    last_name = request.form.get('nom')
    first_name = request.form.get('prenom')
    tel = request.form.get('tel')
    upjv_id = request.form.get('id_upjv')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm = request.form.get('confirm_password')

    user = User.query.filter_by(upjv_id=upjv_id).first()
    if user:
        return error('User already exists')

    if password != confirm:
        return error('Passwords do not match')

    user = User(last_name=last_name,
                first_name=first_name,
                phone_number=tel,
                upjv_id=upjv_id,
                email=email,
                password=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()
    
    login_user(user)
    return redirect(url_for('main.user_profile'))