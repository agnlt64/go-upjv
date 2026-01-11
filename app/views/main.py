import datetime
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request, flash, redirect
from flask_login import logout_user, current_user, login_required
from app.models.ride import Ride 
from app.models.location import Location
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
            # Récupération des données
            nom_depart = request.form.get('start_location')
            nom_arrivee = request.form.get('end_location')
            
            # Récupération des Coordonnées (C'est ça le plus important)
            lat_dep_str = request.form.get('start_lat')
            lon_dep_str = request.form.get('start_lon')
            lat_arr_str = request.form.get('end_lat')
            lon_arr_str = request.form.get('end_lon')

        
            if not lat_dep_str or not lon_dep_str:
                flash("Veuillez ajouter une adresse de départ valide (cliquez sur une suggestion).", "error")
                return redirect(url_for('main.offer_ride'))
            
            if not lat_arr_str or not lon_arr_str:
                flash("Veuillez ajouter une adresse d'arrivée valide (cliquez sur une suggestion).", "error")
                return redirect(url_for('main.offer_ride'))
            

            if lat_dep_str == lat_arr_str and lon_dep_str == lon_arr_str:
                flash("Le point de départ et d'arrivée ne peuvent pas être identiques.", "error")
                return redirect(url_for('main.offer_ride'))
            # ---------------------------

            # Reste du code (Date, Heure, etc.)
            date_str = request.form.get('ride_date')
            heure_str = request.form.get('departure_time')
            seats = request.form.get('seats')
            
            date_heure_depart = datetime.strptime(f"{date_str} {heure_str}", '%Y-%m-%d %H:%M')

            # Gestion Lieu Départ (Plus besoin de valeur par défaut !)
            lieu_depart = Location.query.filter_by(name=nom_depart).first()
            if not lieu_depart:
                lieu_depart = Location(
                    name=nom_depart, 
                    lat=float(lat_dep_str),  # On est sûr que ça existe grâce au if au-dessus
                    lon=float(lon_dep_str), 
                    desc=nom_depart
                )
                db.session.add(lieu_depart)
            
            # Gestion Lieu Arrivée
            lieu_arrivee = Location.query.filter_by(name=nom_arrivee).first()
            if not lieu_arrivee:
                lieu_arrivee = Location(
                    name=nom_arrivee, 
                    lat=float(lat_arr_str), 
                    lon=float(lon_arr_str), 
                    desc=nom_arrivee
                )
                db.session.add(lieu_arrivee)
            
            db.session.commit() # On commit les lieux avant le trajet

            # Création du trajet
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
            flash(f"Erreur : {str(e)}", 'error')

    # Partie GET
    suggestions = Location.query.limit(3).all()
    mes_trajets = Ride.query.filter(Ride.driver_id == current_user.id).all()
    
    return render_template('offer_ride.html', lieux_bdd=suggestions, mes_trajets=mes_trajets)

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
