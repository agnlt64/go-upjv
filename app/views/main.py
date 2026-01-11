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
    # 1. TRAITEMENT DU FORMULAIRE (POST)
    if request.method == 'POST':
        try:
            # Récupération des champs visibles
            nom_depart = request.form.get('start_location')
            nom_arrivee = request.form.get('end_location')
            date_str = request.form.get('ride_date')
            heure_str = request.form.get('departure_time')
            seats = request.form.get('seats')

            # --- MODIFICATION 1 : Récupération des coordonnées cachées ---
            # On récupère ce que le JS a mis dans les input hidden
            lat_dep_str = request.form.get('start_lat')
            lon_dep_str = request.form.get('start_lon')
            lat_arr_str = request.form.get('end_lat')
            lon_arr_str = request.form.get('end_lon')

            # Sécurité : Champs visibles vides
            if not all([nom_depart, nom_arrivee, date_str, heure_str, seats]):
                flash("Veuillez remplir tous les champs obligatoires.", "error")
                return redirect(url_for('main.offer_ride'))

            # Conversion Date/Heure
            date_heure_depart = datetime.strptime(f"{date_str} {heure_str}", '%Y-%m-%d %H:%M')

            # --- MODIFICATION 2 : Gestion Intelligente du Lieu Départ ---
            lieu_depart = Location.query.filter_by(name=nom_depart).first()
            
            if not lieu_depart:
                # Si le lieu n'existe pas, on le crée avec les VRAIES coordonnées
                # Si le JS n'a rien renvoyé (pas de clic), on met une valeur par défaut (Amiens)
                final_lat = float(lat_dep_str) if lat_dep_str else 49.8942
                final_lon = float(lon_dep_str) if lon_dep_str else 2.2958
                
                lieu_depart = Location(
                    name=nom_depart, 
                    lat=final_lat,   # <--- On utilise la variable
                    lon=final_lon,   # <--- On utilise la variable
                    desc="Ajouté par utilisateur"
                )
                db.session.add(lieu_depart)
                db.session.flush()
            else:
                # (Optionnel) Si le lieu existe déjà, on pourrait mettre à jour ses coordonnées
                # si l'utilisateur a sélectionné une adresse plus précise.
                if lat_dep_str and lon_dep_str:
                    lieu_depart.lat = float(lat_dep_str)
                    lieu_depart.lon = float(lon_dep_str)

            # --- MODIFICATION 3 : Gestion Intelligente du Lieu Arrivée ---
            lieu_arrivee = Location.query.filter_by(name=nom_arrivee).first()
            
            if not lieu_arrivee:
                final_lat_arr = float(lat_arr_str) if lat_arr_str else 49.8942
                final_lon_arr = float(lon_arr_str) if lon_arr_str else 2.2958
                
                lieu_arrivee = Location(
                    name=nom_arrivee, 
                    lat=final_lat_arr, 
                    lon=final_lon_arr, 
                    desc="Ajouté par utilisateur"
                )
                db.session.add(lieu_arrivee)
                db.session.flush() 
            else:
                # Mise à jour optionnelle
                if lat_arr_str and lon_arr_str:
                    lieu_arrivee.lat = float(lat_arr_str)
                    lieu_arrivee.lon = float(lon_arr_str)

            # Création du Trajet
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

    # 2. AFFICHAGE DE LA PAGE
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
