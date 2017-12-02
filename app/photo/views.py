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
    #文件保存样例代码
    #filename = f.filename
    #f.save(os.path.join('/root/daizong/', filename))
    #下面据此更改
    upload_image(g.user.user_email, bool(request.form['finished']),
                 f)
    return

@photo_.route('/download', methods=['POST'])
@login_required
def photo_download():
    # TODO
    # 下载文件样例
    # from flask import send_from_directory as sfd
    # sfd(dir, filename)
    # 下面函数为样例，可以修改
    return send_my_file(request.form['email'],
                        bool(request.form['finished']),
                        request.form['image_name'])

@photo_.route('/release_emoji', methods=['POST'])
@login_required
def photo_release_emoji():
    # TODO
    # 根据id修改
    release_emoji(g.user.user_email, request.form['image_name'], request.form['category_name'])
    return jsonify({'type': 'SUCCEED'})

@photo_.route('/get_categories', methods=['POST'])
@login_required
def photo_get_categories():
    # TODO
    # 可能要修正一下上传的格式
    # 比如用jsonify改成json格式
    return get_categories()

@photo_.route('/get_img_by_category_public', methods=['POST'])
@login_required
def photo_get_img_by_category_public():
    # TODO
    # 不知道戴总要不要同时上传图片
    return get_img_by_category_public(request.form['category_name'],
                                      int(request.form['page']))


