from flask_login import login_user, logout_user, current_user, login_required
from flask import Blueprint, g, flash, session, jsonify
from app import lm, db, app
from sql_operation import *

from flask import  request, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash

photo_ = Blueprint('photo', __name__)

@photo_.route('/upload', methods=['POST'])
@login_required
def photo_upload():
    upload_image(g.user.user_email, bool(request.form['finished']),request.form['image_name'],request.form['base64code'])
    return jsionfy({'type':'SUCCEED'})

@photo_.route('/download', methods=['POST'])
@login_required
def photo_download():
    return download_image_to_phone(request.form['image_id'])

@photo_.route('/release_emoji', methods=['POST'])
@login_required
def photo_release_emoji():
    release_emoji(request.form['image_id'], request.form['category_name'])
    return jsonify({'type': 'SUCCEED'})

@photo_.route('/get_categories', methods=['POST'])
@login_required
def photo_get_categories():
    return get_categories()

@photo_.route('/get_img_by_category_public', methods=['POST'])
@login_required
def photo_get_img_by_category_public():
    return get_img_by_category_public(request.form['category_name'],
                                      int(request.form['page']))

