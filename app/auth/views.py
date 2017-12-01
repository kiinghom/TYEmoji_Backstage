from flask_login import login_user, logout_user, current_user, login_required
from flask import Blueprint, g, flash, session
from app import lm, db, app

from flask import  request, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash

auth_ = Blueprint('auth', __name__)

@lm.user_loader
def load_user(id):
    return #TODO

@app.before_request
def before_request():
    g.user = current_user

@auth_.route('/register', methods=['POST'])
def register():
    return render_template('auth/login.html')

@auth_.route('/login', methods=['POST'])
def login():
    return render_template('login.html')

@auth_.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))