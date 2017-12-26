from flask_login import login_user, logout_user, current_user, login_required
from flask import Blueprint, g, flash, session
from app import lm, db, app

from flask import  request, redirect, url_for, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from sql_operation import User, login_func, register_func

auth_ = Blueprint('auth', __name__)

@auth_.route('/register', methods=['GET'])
def register():
    ret = register_func(request.args.get('email'),
                        request.args.get('username'),
                        request.args.get('password'),
                        request.args.get('confirm'))
    return jsonify({'type': ret})

@auth_.route('/login', methods=['GET'])
def login():
    user,ret = login_func(request.args.get('email'), request.args.get('password'),)
    return jsonify({'type': ret})

@auth_.route('/logout', methods=['GET'])
def logout():
    return jsonify({'type': 'SUCCEED'})
