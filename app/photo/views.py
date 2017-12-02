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
    # TODO
    f = request.files['photo']
    upload_image(g.user.user_email, bool(request.form['finished']),
                 f)
    return

@photo_.route('/download', methods=['POST'])
@login_required
def photo_download():
    # TODO
    return send_my_file(request.form['email'],
                        bool(request.form['finished']),
                        request.form['image_name'])

@photo_.route('/release_emoji', methods=['POST'])
@login_required
def photo_release_emoji():
    # TODO
    release_emoji(g.user.user_email, request.form['image_name'], request.form['category_name'])
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


