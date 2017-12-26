from flask_login import login_user, logout_user, current_user, login_required
from flask import Blueprint, g, flash, session, jsonify,Response
from app import lm, db, app
from sql_operation import *
import PIL

from flask import  request, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash

photo_ = Blueprint('photo', __name__)

@photo_.route('/upload', methods=['GET'])
def photo_upload():
    upload_image(request.args.get('email'), bool(request.args.get('finished')),request.args.get('image_name'),request.args.get('base64code'))
    return jsonify({'type':'SUCCEED'})

@photo_.route('/download', methods=['GET'])
def photo_download():
    return jsonify(download_image_to_phone(request.args.get('image_id')))

@photo_.route('/release_emoji', methods=['GET'])
def photo_release_emoji():
    release_emoji(request.args.get('image_id'), request.args.get('category_name'))
    return jsonify({'type': 'SUCCEED'})

@photo_.route('/get_categories', methods=['GET'])
def photo_get_categories():
    return get_categories(request.args.get('screen_height'),request.args.get('screen_width'))

@photo_.route('/get_img_by_category_public', methods=['GET'])
def photo_get_img_by_category_public():
    return jsonify({'data':get_img_by_category_public(request.args.get('category_name'),
                                      int(request.args.get('screen_height')),
                                      int(request.args.get('screen_width')),
                                      int(request.args.get('page')))})

@photo_.route('/get_img_by_user', methods=['GET'])
def photo_get_img_by_user():
    return get_img_by_user(request.args.get('email'),
                                      int(request.args.get('page')))

@photo_.route('/get_popular_img', methods=['GET'])
def photo_get_popular_img():
    return jsonify(get_popular_img(int(request.args.get('page'))))

@photo_.route('/upvote', methods=['GET'])
def photo_upvote():
    upvote(request.args.get('image_id'))
    return jsonify({'type':'SUCCEED'})


@photo_.route('/get_image_by_path', methods=['GET'])
def photo_get_image_by_path():
    height = int(request.args.get('screen_height'))
    width = int(request.args.get('screen_width'))
    img = Image.open(request.args.get('image_path'))
    new_img = img.resize((width,height),Image.ANTIALIAS)
    new_img.save("tempnew.jpg")
    image = file("tempnew.jpg")
    resp=Response(image,mimetype="image/jpeg")
    return resp