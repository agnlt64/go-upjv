from flask import Blueprint, render_template, redirect, url_for
from flask_login import logout_user

main = Blueprint('main', __name__)

@main.route('/')
def index():
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
