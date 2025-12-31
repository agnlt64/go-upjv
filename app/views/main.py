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
            # --- 1. RÉCUPÉRATION DES DONNÉES DU FORMULAIRE ---
            nom_depart = request.form.get('start_location')
            nom_arrivee = request.form.get('end_location')
            date_str = request.form.get('ride_date')         # "2025-12-22"
            heure_str = request.form.get('departure_time')   # "14:30"
            seats = int(request.form.get('seats'))

            # On combine la date et l'heure pour créer un objet datetime complet
            # (Car ta table 'ride' semble avoir une colonne 'date' qui stocke tout)
            date_heure_depart = datetime.strptime(f"{date_str} {heure_str}", '%Y-%m-%d %H:%M')

            # --- 2. GESTION DU LIEU DE DÉPART (Table Location) ---
            # On cherche si ce nom existe déjà dans la table Location
            lieu_depart = Location.query.filter_by(name=nom_depart).first()

            if not lieu_depart:
                # Il n'existe pas, on le crée !
                # Note: On met lat/lon à 0.0 par défaut car on ne les a pas via ce formulaire simple
                lieu_depart = Location(name=nom_depart, lat=49.8942, lon=2.2958, desc="Ajouté par utilisateur")
                db.session.add(lieu_depart)
                db.session.flush() # IMPORTANT: flush() génère l'ID sans fermer la transaction
            
            # --- 3. GESTION DU LIEU D'ARRIVÉE (Table Location) ---
            lieu_arrivee = Location.query.filter_by(name=nom_arrivee).first()

            if not lieu_arrivee:
                lieu_arrivee = Location(name=nom_arrivee, lat=49.8942, lon=2.2958, desc="Ajouté par utilisateur")
                db.session.add(lieu_arrivee)
                db.session.flush() 

            # --- 4. CRÉATION DU TRAJET (Table Ride) ---
            # Maintenant on a lieu_depart.id et lieu_arrivee.id, on peut remplir la table ride
            new_ride = Ride(
                driver_id=current_user.id,
                start_location_id=lieu_depart.id,  # On utilise l'ID récupéré ou créé
                end_location_id=lieu_arrivee.id,   # Idem
                date=date_heure_depart,            # Le datetime complet
                seats=seats
                # Ajoute ici 'price' ou autres colonnes si nécessaire
            )

            db.session.add(new_ride)
            db.session.commit() # On valide tout d'un coup

            flash('Trajet publié avec succès !', 'success')
            return redirect(url_for('mes_trajets')) # Redirige où tu veux

        except Exception as e:
            db.session.rollback() # En cas d'erreur, on annule tout
            flash(f"Erreur lors de l'enregistrement : {str(e)}", 'error')
            print(e) # Affiche l'erreur dans ta console pour le debug

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
