from flask import Blueprint, render_template, redirect, url_for
from flask_login import logout_user, current_user
from app.models.ride import Ride

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.search_ride'))
    return render_template('index.html')

@main.route('/login')
def login():
    return render_template('login.html')

@main.route('/sign-up')
def sign_up():
    return render_template('sign_up.html')

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/user-profile')
def user_profile():
    return render_template('user_profile.html')

@main.route('/offer-ride')
def offer_ride():
    return render_template('offer_ride.html')

@main.route('/my-reservations')
def my_reservations():
    return render_template('my_reservations.html', item=Ride.query.first())

@main.route('/search-ride')
def search_ride():
    return render_template('search_ride.html')
