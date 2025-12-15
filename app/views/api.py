from flask import Blueprint, request, redirect, url_for, flash, render_template, jsonify
from flask_login import login_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from app.models import User, Ride
from sqlalchemy import func
from app.utils import error, success, user_from_request, vehicle_from_request, update, check_password
from app import db

api = Blueprint('api', __name__)

@api.route('/toggle-user/<int:user_id>', methods=['POST'])
@login_required
def toggle_user_status(user_id):
    if not current_user.is_admin:
        return error('Unauthorized', 403)
    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active
    db.session.commit()
    
    return success('ok')

@api.route('/toggle-admin/<int:user_id>', methods=['POST'])
@login_required
def toggle_admin_role(user_id):
    if not current_user.is_admin:
        return error('Unauthorized', 403)
    user = User.query.get_or_404(user_id)
    user.is_admin = not user.is_admin
    db.session.commit()
    
    return success('ok')

@api.route('/login', methods=['POST'])
def login():
    password = request.form.get('password')
    
    user = user_from_request()

    if actual_user := user.exists():
        if not actual_user.is_active:
            flash('Your account was deactivated', 'error')
            return render_template('auth/login.html', user=actual_user)
        if check_password_hash(actual_user.password, password):
            login_user(actual_user)
            return redirect(url_for('main.user_profile'))
        else:
            flash('Invalid password', 'error')
            return render_template('auth/login.html', user=user)

    flash('User not found', 'error')
    return render_template('auth/login.html', user=user)

@api.route('/sign-up', methods=['POST'])
def sign_up():
    password = request.form.get('password')
    confirm = request.form.get('confirm_password')

    user = user_from_request()

    if user.exists():
        flash('UPJV ID or email already in use', 'error')
        return render_template('auth/sign_up.html', user=user)

    if password != confirm:
        flash('Passwords do not match', 'error')
        return render_template('auth/sign_up.html', user=user)
    
    if not user.is_valid():
        return render_template('auth/sign_up.html', user=user)
    
    if not check_password(password):
        return render_template('auth/sign_up.html', user=user)
    
    user.password = generate_password_hash(password)
    db.session.add(user)
    db.session.commit()
    
    login_user(user)
    return redirect(url_for('main.user_profile'))

@api.route('/update-profile', methods=['POST'])
@login_required
def update_profile():
    user = user_from_request()
    if user.is_valid():
        update(current_user, user)
        db.session.commit()
        flash('Profile updated successfully', 'success')
    return redirect(url_for('main.user_profile'))

@api.route('/update-vehicle', methods=['POST'])
@login_required
def update_vehicle():
    vehicle = vehicle_from_request()
    if vehicle.is_valid():
        update(current_user.vehicle, vehicle)
        db.session.commit()
        flash('Vehicle updated successfully', 'success')
    return redirect(url_for('main.user_profile'))

@api.route('/add-vehicle', methods=['PUT', 'POST'])
@login_required
def add_vehicle():
    vehicle = vehicle_from_request()
    if vehicle.is_valid():
        vehicle.owner_id = current_user.id
        db.session.add(vehicle)
        db.session.commit()
        flash('Vehicle added successfully', 'success')
    else:
        flash('Invalid vehicle data', 'error')
    return redirect(url_for('main.user_profile'))

@api.route('/delete-vehicle', methods=['DELETE', 'POST'])
@login_required
def delete_vehicle():
    vehicle = current_user.vehicle
    if vehicle:
        db.session.delete(vehicle)
        db.session.commit()
        flash('Vehicle deleted successfully', 'success')
    else:
        flash('brochacho reached unreachable code 🥀', 'error')
    return redirect(url_for('main.user_profile'))

@api.route('/change-password', methods=['PATCH', 'POST'])
@login_required
def change_password():
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_new_password')

    if not check_password_hash(current_user.password, current_password):
        flash('Current password is incorrect', 'error')
        return redirect(url_for('main.user_profile'))

    if new_password != confirm_password:
        flash('New passwords do not match', 'error')
        return redirect(url_for('main.user_profile'))

    if not check_password(new_password):
        flash('New password does not meet requirements', 'error')
        return redirect(url_for('main.user_profile'))

    current_user.password = generate_password_hash(new_password)
    db.session.commit()
    flash('Password changed successfully', 'success')
    return redirect(url_for('main.user_profile'))


@api.route('/rides/<int:ride_id>/passengers', methods=['GET'])
@login_required
def ride_passengers(ride_id):
    """Retourne la liste des passagers pour le trajet demandé en JSON.
    Requiert authentification.
    """
    ride = Ride.query.get_or_404(ride_id)

    # Compute required number: res = 3 - seats
    seats = int(ride.seats) if ride.seats is not None else 0
    res = max(0, 3 - seats)
    if res <= 0:
        return jsonify({'status': 200, 'success': True, 'passengers': []})

    # exclude driver from the random selection
    query = User.query.filter(User.id != ride.driver_id)
    # do not request more users than exist
    try:
        available = query.count()
    except Exception:
        available = None

    limit = res if (available is None or res <= available) else available
    random_users = query.order_by(func.random()).limit(limit).all()

    passengers = []
    for p in random_users:
        display = p.to_str() if hasattr(p, 'to_str') and callable(p.to_str) else f"{p.first_name} {p.last_name}".strip()
        passengers.append({
            'id': p.id,
            'name': display,
            'upjv_id': getattr(p, 'upjv_id', None)
        })

    return jsonify({'status': 200, 'success': True, 'passengers': passengers})