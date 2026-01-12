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

@main.route('/search-ride')
@login_required
def search_ride():
    return render_template('search_ride.html')
