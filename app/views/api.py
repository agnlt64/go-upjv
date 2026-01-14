from flask import Blueprint, request, redirect, url_for, flash, render_template, jsonify, current_app
from flask_login import login_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import uuid
import os

from app.models import User, Ride, Review
from app.models.location import Location
from app.utils import error, success, user_from_request, vehicle_from_request, update, check_password, distance
from app import db
from flask import jsonify, request

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_vehicle_image(file):
    if file and file.filename and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'vehicles')
        os.makedirs(upload_folder, exist_ok=True)
        file.save(os.path.join(upload_folder, unique_filename))
        return unique_filename
    return None

api = Blueprint('api', __name__)

@api.route('/toggle-user/<int:user_id>', methods=['POST'])
@login_required
def toggle_user_status(user_id):
    if not current_user.is_admin: return error('Unauthorized', 403)
    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active
    db.session.commit()
    return success('ok')

@api.route('/toggle-admin/<int:user_id>', methods=['POST'])
@login_required
def toggle_admin_role(user_id):
    if not current_user.is_admin: return error('Unauthorized', 403)
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
            return redirect(url_for('main.settings'))
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
        flash('UPJV ID already in use', 'error')
        return render_template('auth/sign_up.html', user=user)
    if password != confirm:
        flash('Passwords do not match', 'error')
        return render_template('auth/sign_up.html', user=user)
    if not user.is_valid(): return render_template('auth/sign_up.html', user=user)
    if not check_password(password): return render_template('auth/sign_up.html', user=user)
    user.password = generate_password_hash(password)
    db.session.add(user)
    db.session.commit()
    login_user(user)
    return redirect(url_for('main.settings'))

@api.route('/update-profile', methods=['POST'])
@login_required
def update_profile():
    user = user_from_request()
    if user.is_valid():
        update(current_user, user)
        db.session.commit()
        flash('Profile updated successfully', 'success')
    return redirect(url_for('main.settings'))

@api.route('/update-vehicle', methods=['POST'])
@login_required
def update_vehicle():
    vehicle = vehicle_from_request()
    if vehicle.is_valid():
        update(current_user.vehicle, vehicle)
        
        # Handle image upload
        if 'vehicle_image' in request.files:
            image_path = save_vehicle_image(request.files['vehicle_image'])
            if image_path:
                # Delete old image if exists
                if current_user.vehicle.image_path:
                    old_path = os.path.join(current_app.root_path, 'static', 'uploads', 'vehicles', current_user.vehicle.image_path)
                    if os.path.exists(old_path):
                        os.remove(old_path)
                current_user.vehicle.image_path = image_path
        
        db.session.commit()
        flash('Vehicle updated successfully', 'success')
    return redirect(url_for('main.settings'))

@api.route('/add-vehicle', methods=['PUT', 'POST'])
@login_required
def add_vehicle():
    vehicle = vehicle_from_request()
    if vehicle.is_valid():
        # Handle image upload
        if 'vehicle_image' in request.files:
            image_path = save_vehicle_image(request.files['vehicle_image'])
            if image_path:
                vehicle.image_path = image_path
        
        vehicle.owner_id = current_user.id
        db.session.add(vehicle)
        db.session.commit()
        flash('Vehicle added successfully', 'success')
    else: flash('Invalid vehicle data', 'error')
    return redirect(url_for('main.settings'))

@api.route('/delete-vehicle', methods=['DELETE', 'POST'])
@login_required
def delete_vehicle():
    vehicle = current_user.vehicle
    if vehicle:
        db.session.delete(vehicle)
        db.session.commit()
        flash('Vehicle deleted successfully', 'success')
    else: flash('brochacho reached unreachable code 🥀', 'error')
    return redirect(url_for('main.settings'))

@api.route('/change-password', methods=['PATCH', 'POST'])
@login_required
def change_password():
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_new_password')
    if not check_password_hash(current_user.password, current_password):
        flash('Current password is incorrect', 'error')
        return redirect(url_for('main.settings'))
    if new_password != confirm_password:
        flash('New passwords do not match', 'error')
        return redirect(url_for('main.settings'))
    if not check_password(new_password):
        flash('New password does not meet requirements', 'error')
        return redirect(url_for('main.settings'))
    current_user.password = generate_password_hash(new_password)
    db.session.commit()
    flash('Password changed successfully', 'success')
    return redirect(url_for('main.settings'))

@api.route('/search-rides', methods=['GET'])
@login_required
def search_rides():
    now = datetime.now()
    user_lat = request.args.get('lat', type=float)
    user_lon = request.args.get('lon', type=float)
    rides_query = Ride.query.filter(Ride.date >= now, Ride.seats > 0).all()
    results = []
    for ride in rides_query:
        dist_km = 0
        if user_lat and user_lon and ride.start_location:
            user_loc = Location(lat=user_lat, lon=user_lon)
            dist_km = distance(user_loc, ride.start_location)
        driver_name = f"{ride.driver.first_name} {ride.driver.last_name}" if ride.driver else "Inconnu"
        start_name = ride.start_location.name if ride.start_location else "Départ inconnu"
        end_name = ride.end_location.name if ride.end_location else "Arrivée inconnue"
        results.append({
            'id': ride.id,
            'driver_name': driver_name,
            'date_day': ride.date.strftime('%d'),
            'date_month': ride.date.strftime('%b'),
            'date_year': ride.date.strftime('%Y'),
            'time_start': ride.date.strftime('%H:%M'),
            'time_end': (ride.date + timedelta(hours=1)).strftime('%H:%M'),
            'departure': start_name,
            'arrival': end_name,
            'start_lat': ride.start_location.lat if ride.start_location else None,
            'start_lon': ride.start_location.lon if ride.start_location else None,
            'end_lat': ride.end_location.lat if ride.end_location else None,
            'end_lon': ride.end_location.lon if ride.end_location else None,
            'seats': ride.seats,
            'distance': dist_km
        })
    if user_lat and user_lon:
        results.sort(key=lambda x: x['distance'])
        results = results[:5]
    else:
        results.sort(key=lambda x: (x['date_year'], x['date_month'], x['date_day'], x['time_start']))
    return jsonify({'success': True, 'rides': results})

@api.route('/book-ride/<int:ride_id>', methods=['POST'])
@login_required
def book_ride(ride_id):
    ride = Ride.query.get_or_404(ride_id)
    if ride.seats <= 0:
        flash('Ce trajet est complet !', 'error')
        return redirect(url_for('main.search_ride'))
    if ride.driver_id == current_user.id:
        flash('Impossible de réserver son propre trajet.', 'error')
        return redirect(url_for('main.search_ride'))
    if current_user in ride.passengers:
        flash('Vous avez déjà réservé ce trajet.', 'error')
        return redirect(url_for('main.search_ride'))
    ride.passengers.append(current_user)
    ride.seats -= 1
    db.session.commit()
    flash('Réservation enregistrée avec succès !', 'success')
    return redirect(url_for('main.search_ride'))

@api.route('/cancel-ride/<int:ride_id>', methods=['POST'])
@login_required
def cancel_ride(ride_id):
    ride = Ride.query.get_or_404(ride_id)
    
    if ride.driver_id != current_user.id:
        flash('Vous ne pouvez annuler que vos propres trajets.', 'error')
        return redirect(url_for('main.offer_ride'))
    
    if ride.is_cancelled:
        flash('Ce trajet est déjà annulé.', 'error')
        return redirect(url_for('main.offer_ride'))
    
    if ride.date < datetime.now():
        flash('Impossible d\'annuler un trajet passé.', 'error')
        return redirect(url_for('main.offer_ride'))
    
    ride.is_cancelled = True
    db.session.commit()
    
    flash('Trajet annulé avec succès.', 'success')
    return redirect(url_for('main.offer_ride'))

@api.route('/rides/<int:ride_id>/passengers')
@login_required
def get_ride_passengers(ride_id):
    ride = Ride.query.get_or_404(ride_id)
    users = ride.passengers
    liste_passagers = []
    
    for user in users:
        full_name = f"{user.first_name} {user.last_name}"
        
        liste_passagers.append({
            'name': full_name,
            'upjv_id': user.upjv_id,
            'avatar_initial': user.first_name[0].upper() if user.first_name else "?"
        })
    
    return jsonify({'passengers': liste_passagers})

@api.route('/submit-review', methods=['POST'])
@login_required
def submit_review():
    data = request.get_json()
    ride_id = data.get('ride_id')
    target_id = data.get('target_id')
    rating = data.get('rating')
    content = data.get('content', '')
    
    if not all([ride_id, target_id, rating]):
        return error('Données manquantes', 400)
    
    try:
        rating = int(rating)
        if rating < 1 or rating > 5:
            return error('La note doit être entre 1 et 5', 400)
    except (ValueError, TypeError):
        return error('Note invalide', 400)
    
    ride = Ride.query.get_or_404(ride_id)
    target = User.query.get_or_404(target_id)
    
    if ride.date > datetime.now():
        return error('Ce trajet n\'est pas encore terminé', 400)
    
    is_passenger = current_user in ride.passengers
    is_driver = ride.driver_id == current_user.id
    
    if not is_passenger and not is_driver:
        return error('Vous n\'avez pas participé à ce trajet', 403)
    
    if is_passenger and target_id != ride.driver_id:
        return error('En tant que passager, vous ne pouvez noter que le conducteur', 400)
    
    if is_driver and target not in ride.passengers:
        return error('Vous ne pouvez noter que les passagers de ce trajet', 400)
    
    existing = Review.query.filter_by(
        ride_id=ride_id,
        author_id=current_user.id,
        target_id=target_id
    ).first()
    
    if existing:
        return error('Vous avez déjà noté cette personne pour ce trajet', 400)
    
    review = Review(
        ride_id=ride_id,
        author_id=current_user.id,
        target_id=target_id,
        rating=rating,
        content=content
    )
    
    db.session.add(review)
    db.session.commit()
    
    return success('Avis enregistré avec succès')

@api.route('/reviews/<int:review_id>', methods=['DELETE'])
@login_required
def delete_review(review_id):
    if not current_user.is_admin:
        return error('Unauthorized', 403)
    
    review = Review.query.get_or_404(review_id)
    db.session.delete(review)
    db.session.commit()
    
    return success('Avis supprimé avec succès')