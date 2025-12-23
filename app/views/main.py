import datetime
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for
from flask_login import logout_user, current_user, login_required
from app.models.ride import Ride 
from app.models.location import Location


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

@main.route('/user-profile')
@login_required
def user_profile():
    return render_template('user_profile.html')
    

@main.route('/offer-ride')
@login_required

def offer_ride():

    suggestions = Location.query.limit(3).all()
    return render_template('offer_ride.html', lieux_bdd=suggestions)

@main.route('/my-reservations')
@login_required
def my_reservations():
    now = datetime.now()
    # Séparation des trajets à venir et passés
    upcoming_rides = Ride.query.filter(Ride.date > now).order_by(Ride.date.asc()).all()
    past_rides = Ride.query.filter(Ride.date < now).order_by(Ride.date.asc()).all()
    return render_template('my_reservations.html', upcoming_rides=upcoming_rides, past_rides=past_rides)

# --- AJOUT DE LA ROUTE MANQUANTE ---
@main.route('/search-ride')
@login_required
def search_ride():
    return render_template('search_ride.html')




from app.models import Ride, User 


@main.route('/rides/<int:ride_id>/passengers')
@login_required
def get_ride_passengers(ride_id):
    # 1. On récupère le trajet
    ride = Ride.query.get_or_404(ride_id)
    
    # 2. On récupère les passagers
    users = ride.passengers
    
    # 3. On prépare le JSON
    liste_passagers = []
    
    for user in users:
        full_name = f"{user.first_name} {user.last_name}"
        
        liste_passagers.append({
            'name': full_name,
            'upjv_id': user.upjv_id,
            'avatar_initial': user.first_name[0].upper() if user.first_name else "?"
        })
    
    return jsonify({'passengers': liste_passagers})
