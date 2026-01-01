from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, request, flash, redirect, jsonify
from flask_login import logout_user, current_user, login_required

from app.models.ride import Ride
from app.models.location import Location
from app.models.ride import Ride
from app import db


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
    

@main.route('/offer-ride', methods=['GET', 'POST'])
@login_required
def offer_ride():
    if request.method == 'POST':
        try:
            nom_depart = request.form.get('start_location')
            nom_arrivee = request.form.get('end_location')
            date_str = request.form.get('ride_date')
            heure_str = request.form.get('departure_time')
            seats = request.form.get('seats')

            if not all([nom_depart, nom_arrivee, date_str, heure_str, seats]):
                flash("Veuillez remplir tous les champs obligatoires.", "error")
                return redirect(url_for('main.offer_ride'))

            date_heure_depart = datetime.strptime(f"{date_str} {heure_str}", '%Y-%m-%d %H:%M')

            lieu_depart = Location.query.filter_by(name=nom_depart).first()
            if not lieu_depart:
                lieu_depart = Location(name=nom_depart, lat=49.8942, lon=2.2958, desc="Ajouté par utilisateur")
                db.session.add(lieu_depart)
                db.session.flush()
            
            lieu_arrivee = Location.query.filter_by(name=nom_arrivee).first()
            if not lieu_arrivee:
                lieu_arrivee = Location(name=nom_arrivee, lat=49.8942, lon=2.2958, desc="Ajouté par utilisateur")
                db.session.add(lieu_arrivee)
                db.session.flush() 

            new_ride = Ride(
                driver_id=current_user.id,
                start_location_id=lieu_depart.id,
                end_location_id=lieu_arrivee.id,
                date=date_heure_depart,
                seats=int(seats)
            )

            db.session.add(new_ride)
            db.session.commit()

            flash('Trajet publié avec succès !', 'success')
            return redirect(url_for('main.offer_ride'))

        except Exception as e:
            db.session.rollback()
            flash(f"Erreur technique : {str(e)}", 'error')
            print(f"DEBUG ERROR: {e}")

    suggestions = Location.query.limit(3).all()

    mes_trajets = Ride.query.filter(
        Ride.driver_id == current_user.id,        
        Ride.date >= datetime.now()
    ).order_by(Ride.date.asc()).all()             
    return render_template('offer_ride.html', 
                           lieux_bdd=suggestions,
                           mes_trajets=mes_trajets)

@main.route('/my-reservations')
@login_required
def my_reservations():
    now = datetime.now()
    upcoming_rides = Ride.query.filter(Ride.date > now).order_by(Ride.date.asc()).all()
    past_rides = Ride.query.filter(Ride.date < now).order_by(Ride.date.asc()).all()
    return render_template('my_reservations.html', upcoming_rides=upcoming_rides, past_rides=past_rides)

@main.route('/search-ride')
@login_required
def search_ride():
    return render_template('search_ride.html')

@main.route('/rides/<int:ride_id>/passengers')
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
