from flask_login import login_user, logout_user, current_user, login_required
from flask import Blueprint, g, flash, session
from app import lm, db, app
import json

from flask import  request, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash

photo_ = Blueprint('photo', __name__)

@app.before_request
def before_request():
    g.user = current_user

@photo_.route('/upload', methods=['POST'])
def photo_upload():
    f = request.files['photo']
    # TODO
    return

@photo_.route('/download', methods=['POST'])
def photo_download():
    return jsonify()
