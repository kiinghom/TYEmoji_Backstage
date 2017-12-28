# -*- coding: utf-8 -*-
from flask_login import login_user, logout_user, current_user, login_required
from flask import Blueprint, g, flash, session, jsonify,Response
from app import lm, db, app
from sql_operation import *
import PIL

from flask import  request, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash

photo_ = Blueprint('photo', __name__)

@photo_.route('/upload', methods=['POST'])
def photo_upload():
    upload_image(request.form['user_id'], bool(request.form['finished']),request.form['image_name'],request.form['base64code'])
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
    return jsonify({'data':get_img_by_user(request.args.get('email'),
        int(request.args.get('screen_height')),
        int(request.args.get('screen_width')),
        int(request.args.get('page')))})

@photo_.route('/get_img_by_upvote', methods=['GET'])
def photo_get_img_by_upvote():
    return jsonify({"useTime": [0.152028],
    "slider": [
        {
            "type": "special",
            "name": "壹周壁纸精选集",
            "detail": "http://api.lovebizhi.com/android_v3.php?a=special&special_id=803&spdy=1&slider=home&device=random&uuid=random&mode=2&client_id=1001&device_id=0&model_id=100&size_id=0&channel_id=26&screen_width=1080&screen_height=1920&bizhi_width=1080&bizhi_height=1920&version_code=75&language=zh-CN&mac=&original=0",
            "analyze": "http://position.lovebizhi.com/analyze.php?id=3812&client_id=1001&device_id=0&user_id=0",
            "image": "http://s.qdcdn.com/cc/14540558.webp"
        },
        {
            "type": "special",
            "name": "轻盈的背影",
            "detail": "http://api.lovebizhi.com/android_v3.php?a=special&special_id=801&spdy=1&slider=home&device=random&uuid=random&mode=2&client_id=1001&device_id=0&model_id=100&size_id=0&channel_id=26&screen_width=1080&screen_height=1920&bizhi_width=1080&bizhi_height=1920&version_code=75&language=zh-CN&mac=&original=0",
            "analyze": "http://position.lovebizhi.com/analyze.php?id=3805&client_id=1001&device_id=0&user_id=0",
            "image": "http://s.qdcdn.com/cc/14534297.webp"
        },
        {
            "type": "special",
            "name": "壹周壁纸精选集",
            "detail": "http://api.lovebizhi.com/android_v3.php?a=special&special_id=799&spdy=1&slider=home&device=random&uuid=random&mode=2&client_id=1001&device_id=0&model_id=100&size_id=0&channel_id=26&screen_width=1080&screen_height=1920&bizhi_width=1080&bizhi_height=1920&version_code=75&language=zh-CN&mac=&original=0",
            "analyze": "http://position.lovebizhi.com/analyze.php?id=3799&client_id=1001&device_id=0&user_id=0",
            "image": "http://s.qdcdn.com/cc/14529206.webp"
        },
        {
            "type": "special",
            "name": "滴水美景",
            "detail": "http://api.lovebizhi.com/android_v3.php?a=special&special_id=798&spdy=1&slider=home&device=random&uuid=random&mode=2&client_id=1001&device_id=0&model_id=100&size_id=0&channel_id=26&screen_width=1080&screen_height=1920&bizhi_width=1080&bizhi_height=1920&version_code=75&language=zh-CN&mac=&original=0",
            "analyze": "http://position.lovebizhi.com/analyze.php?id=3793&client_id=1001&device_id=0&user_id=0",
            "image": "http://s.qdcdn.com/cc/14522732.webp"
        },
        {
            "type": "special",
            "name": "城堡王国",
            "detail": "http://api.lovebizhi.com/android_v3.php?a=special&special_id=794&spdy=1&slider=home&device=random&uuid=random&mode=2&client_id=1001&device_id=0&model_id=100&size_id=0&channel_id=26&screen_width=1080&screen_height=1920&bizhi_width=1080&bizhi_height=1920&version_code=75&language=zh-CN&mac=&original=0",
            "analyze": "http://position.lovebizhi.com/analyze.php?id=3780&client_id=1001&device_id=0&user_id=0",
            "image": "http://s.qdcdn.com/cc/14515602.webp"
        }
    ],
    "link": {
        "prev": "",
        "self": "http://api.lovebizhi.com/android_v3.php?a=home&mode=2&client_id=1001&model_id=100&channel_id=26&size_id=0&spdy=1&version_code=75&language=zh-CN&mac=&original=0&device=random&uuid=random&device_id=random&screen_width=1080&screen_height=1920&bizhi_width=1080&bizhi_height=1920&p=1",
        "next": "http://api.lovebizhi.com/android_v3.php?a=home&spdy=1&device=random&uuid=random&mode=2&client_id=1001&device_id=0&model_id=100&size_id=0&channel_id=26&screen_width=1080&screen_height=1920&bizhi_width=1080&bizhi_height=1920&version_code=75&language=zh-CN&mac=&original=0&p=2"
    },
    	'data':get_img_by_upvote(int(request.args.get('screen_height')),
        int(request.args.get('screen_width')),
        int(request.args.get('page')))})


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