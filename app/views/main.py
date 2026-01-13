from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, request, flash, redirect, jsonify
from flask_login import logout_user, current_user, login_required

from app.models.ride import Ride
from app.models.location import Location
from app.models.ride import Ride
from app import db
from app.utils import (
    validate_ride_data,
    get_or_create_location,
    create_ride,
    get_user_rides,
    get_location_suggestions
)


main = Blueprint('main', __name__)

@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.search_ride'))
    return render_template('index.html')

@main.route('/login')
def login():
    return render_template('auth/login.html')

@main.route('/sign-up')
def sign_up():
    return render_template('auth/sign_up.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/settings')
@login_required
def settings():
    return render_template('settings.html')

@main.route('/search-ride')
@login_required
def search_ride():
    now = datetime.now()
    rides = Ride.query.filter(Ride.date >= now, Ride.seats > 0).order_by(Ride.date.asc()).all()
    return render_template('search_ride.html', rides=rides)

@main.route('/my-reservations')
@login_required
def my_reservations():
    now = datetime.now()
    upcoming_rides = Ride.query.filter(Ride.date > now, Ride.passengers.contains(current_user)).order_by(Ride.date.asc())
    past_rides = Ride.query.filter(Ride.date < now, Ride.passengers.contains(current_user)).order_by(Ride.date.desc())
    
    from app.models import Review
    reviewed_rides = {}
    for ride in past_rides:
        existing = Review.query.filter_by(
            ride_id=ride.id,
            author_id=current_user.id,
            target_id=ride.driver_id
        ).first()
        reviewed_rides[ride.id] = existing is not None

    return render_template('my_reservations.html', 
                           upcoming_rides=upcoming_rides, 
                           past_rides=past_rides,
                           reviewed_rides=reviewed_rides)


@main.route('/offer-ride', methods=['GET', 'POST'])
@login_required
def offer_ride():
    if request.method == 'POST':
        try:
            ride_data = validate_ride_data()
            if not ride_data:
                return redirect(url_for('main.offer_ride'))

            lieu_depart = get_or_create_location(
                ride_data['nom_depart'],
                ride_data['lat_dep'],
                ride_data['lon_dep'],
                ride_data['nom_depart']
            )
            
            lieu_arrivee = get_or_create_location(
                ride_data['nom_arrivee'],
                ride_data['lat_arr'],
                ride_data['lon_arr'],
                ride_data['nom_arrivee']
            )

            create_ride(
                current_user.id,
                lieu_depart.id,
                lieu_arrivee.id,
                ride_data['date_heure_depart'],
                ride_data['seats']
            )

            flash('Trajet publié avec succès !', 'success')
            return redirect(url_for('main.offer_ride'))

        except Exception as e:
            db.session.rollback()
            flash(f"Erreur : {str(e)}", 'error')

    suggestions = get_location_suggestions()
    mes_trajets = get_user_rides(current_user.id)
    
    return render_template('offer_ride.html', lieux_bdd=suggestions, mes_trajets=mes_trajets)

@main.route('/user/<upjv_id>')
def public_profile(upjv_id):
    from app.models import User, Review
    
    user = User.query.filter_by(upjv_id=upjv_id).first_or_404()
    
    reviews = Review.query.filter_by(target_id=user.id).order_by(Review.id.desc()).all()
    
    avg_rating = None
    if reviews:
        avg_rating = sum(r.rating for r in reviews) / len(reviews)
    
    is_driver = len(user.rides_driven) > 0
    
    return render_template('public_profile.html', 
                           profile_user=user, 
                           reviews=reviews,
                           avg_rating=avg_rating,
                           is_driver=is_driver)

