from flask import jsonify, request, flash

from math import radians, sin, cos, sqrt, atan2
import re
from datetime import datetime

from app.models.location import Location

UPJV_ID_REGEX = r'^[a-zA-Z][0-9]{8}$'
PASSWORD_REGEX = r'^(?=.*[a-zA-Z])(?!.*\s)(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>]).{8,}$'
EMAIL_REGEX = r'^[a-zA-Z]+\.[a-zA-Z]+@([a-zA-Z0-9-]+\.)?u-picardie\.fr$'
PHONE_REGEX = r'^[0-9]{10}$'

LICENCE_PLATE_1 = r'^[A-HJ-NP-TV-Z]{2}-[0-9]{3}-[A-HJ-NP-TV-Z]{2}$'
LICENCE_PLATE_2 = r'^[0-9]{1,4} [A-Z]{1,3} [0-9]{2}$'

def error(message: str, status=500):
    return jsonify({
        'status': status,
        'success': False,
        'message': message
    })

def success(message: str):
    return jsonify({
        'status': 200,
        'success': True,
        'message': message
    })

def check_email(email: str):
    return re.match(EMAIL_REGEX, email)

def check_password(password: str):
    return re.match(PASSWORD_REGEX, password)

def check_upjv_id(upjv_id: str):
    return re.match(UPJV_ID_REGEX, upjv_id)

def check_phone(phone: str):
    return re.match(PHONE_REGEX, phone)

def check_licence_plate(licence_plate: str):
    return re.match(LICENCE_PLATE_1, licence_plate) or re.match(LICENCE_PLATE_2, licence_plate)

def distance(from_: Location, to: Location) -> float:
    R = 6371.0
    lat1 = from_.lat
    lon1 = from_.lon
    lat2 = to.lat
    lon2 = to.lon

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

def int_to_month(n: int) -> str:
    months = [
        "JAN", "FEV", "MAR", "AVR", "MAI", "JUN",
        "JUI", "AOUT", "SEP", "OCT", "NOV", "DEC"
    ]
    if 1 <= n <= 12:
        return months[n - 1]
    return ""

def update(what, to):
    for key, value in to.__dict__.items():
        if not key.startswith('_') and key != 'id':
            setattr(what, key, value)

def user_from_request():
    from app.models.user import User
    
    last_name = request.form.get('last_name')
    first_name = request.form.get('first_name')
    tel = request.form.get('phone_number')
    upjv_id = request.form.get('upjv_id')
    email = request.form.get('email')
    password = request.form.get('password')
    bio = request.form.get('bio')
    
    user = User(last_name=last_name,
                first_name=first_name,
                phone_number=tel,
                upjv_id=upjv_id,
                email=email,
                bio=bio)
    
    if tel and not check_phone(tel):
        flash('Invalid phone number', 'error')
        user.phone_number = ''
    if upjv_id and not check_upjv_id(upjv_id):
        flash('Invalid UPJV ID', 'error')
        user.upjv_id = ''
    if email and not check_email(email):
        flash('Invalid email', 'error')
        user.email = ''
    if password and not check_password(password):
        flash('Password doesn\'t match requirements', 'error')

    return user

def vehicle_from_request():
    from app.models.vehicle import Vehicle
    
    model = request.form.get('model')
    color = request.form.get('color')
    licence_plate = request.form.get('licence_plate')
    max_seats = request.form.get('max_seats')
    
    vehicle = Vehicle(model=model,
                      color=color,
                      licence_plate=licence_plate)
    
    if licence_plate and not check_licence_plate(licence_plate):
        flash('Invalid licence plate', 'error')
        vehicle.licence_plate = ''
    
    try:
        vehicle.max_seats = int(max_seats)
    except (ValueError, TypeError):
        flash('Max seats must be a number', 'error')
        vehicle.max_seats = None
    
    return vehicle

def validate_ride_data():
    """Valide et retourne les données du formulaire pour un trajet"""
    nom_depart = request.form.get('start_location')
    nom_arrivee = request.form.get('end_location')
    
    lat_dep_str = request.form.get('start_lat')
    lon_dep_str = request.form.get('start_lon')
    lat_arr_str = request.form.get('end_lat')
    lon_arr_str = request.form.get('end_lon')

    if not lat_dep_str or not lon_dep_str:
        flash("Veuillez ajouter une adresse de départ valide (cliquez sur une suggestion).", "error")
        return None
    
    if not lat_arr_str or not lon_arr_str:
        flash("Veuillez ajouter une adresse d'arrivée valide (cliquez sur une suggestion).", "error")
        return None
    
    if lat_dep_str == lat_arr_str and lon_dep_str == lon_arr_str:
        flash("Le point de départ et d'arrivée ne peuvent pas être identiques.", "error")
        return None

    date_str = request.form.get('ride_date')
    heure_str = request.form.get('departure_time')
    seats = request.form.get('seats')
    
    try:
        date_heure_depart = datetime.strptime(f"{date_str} {heure_str}", '%Y-%m-%d %H:%M')
    except (ValueError, TypeError):
        flash("Format de date ou heure invalide.", "error")
        return None

    if date_heure_depart < datetime.now():
        flash("Vous ne pouvez pas proposer un trajet dans le passé !", "error")
        return None

    try:
        seats = int(seats)
    except (ValueError, TypeError):
        flash("Le nombre de places doit être un nombre valide.", "error")
        return None

    return {
        'nom_depart': nom_depart,
        'nom_arrivee': nom_arrivee,
        'lat_dep': float(lat_dep_str),
        'lon_dep': float(lon_dep_str),
        'lat_arr': float(lat_arr_str),
        'lon_arr': float(lon_arr_str),
        'date_heure_depart': date_heure_depart,
        'seats': seats
    }

def get_or_create_location(name, lat, lon, desc):
    """Récupère ou crée un lieu"""
    from app import db
    
    lieu = Location.query.filter_by(name=name).first()
    if not lieu:
        lieu = Location(name=name, lat=lat, lon=lon, desc=desc)
        db.session.add(lieu)
        db.session.flush()
    return lieu

def create_ride(driver_id, start_location_id, end_location_id, date, seats):
    """Crée un nouveau trajet"""
    from app import db
    from app.models.ride import Ride
    
    new_ride = Ride(
        driver_id=driver_id,
        start_location_id=start_location_id,
        end_location_id=end_location_id,
        date=date,
        seats=seats
    )
    db.session.add(new_ride)
    db.session.commit()
    return new_ride

def get_user_rides(user_id):
    """Récupère tous les trajets d'un utilisateur"""
    from app.models.ride import Ride
    return Ride.query.filter(Ride.driver_id == user_id).all()

def get_location_suggestions(limit=3):
    """Récupère des suggestions de lieux"""
    return Location.query.limit(limit).all()