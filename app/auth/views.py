from flask_login import login_user, logout_user, current_user, login_required
from flask import Blueprint, g, flash, session
from app import lm, db, app

from flask import  request, redirect, url_for, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from sql_operation import User, login_func, register_func

auth_ = Blueprint('auth', __name__)

@lm.user_loader
def load_user(id):
    return User.query.filter_by(user_email=str(id)).first()

@app.before_request
def before_request():
    g.user = current_user

@auth_.route('/register', methods=['POST'])
def register():
    ret = register_func(request.form['email'],
                        request.form['username'],
                        request.form['password'],
                        request.form['confirm'])
    return jsonify({
        'type': ret
    })

@auth_.route('/login', methods=['POST'])
def login():
    user,ret = login_func(request.form['email'],request.form['password'])
    if user != None:
        login_user(user)
    return jsonify({
        'type': ret
    })

@auth_.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return jsonify({
        'type': 'SUCCEED'
    })
