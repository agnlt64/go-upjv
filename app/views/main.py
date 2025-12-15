import datetime
from flask import Blueprint, render_template, redirect, url_for
from flask_login import logout_user, current_user, login_required
from app.models.ride import Ride
from datetime import datetime

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
    return render_template('offer_ride.html')

@main.route('/my-reservations')
@login_required
def my_reservations():

    humain = Ride.query.limit(3).all()#Place la limite a 3 pour le a venir

    actuel=datetime.now()
    futur = Ride.query.filter(Ride.date > actuel)\
                        .order_by(Ride.date.asc())\
                        .limit(2).all()

    passee = Ride.query.filter(Ride.date < actuel)\
                        .order_by(Ride.date.asc())\
                        .limit(3).all()
    return render_template('my_reservations.html', item=futur, test=passee)

@main.route('/search-ride')
@login_required
def search_ride():
    return render_template('search_ride.html')
