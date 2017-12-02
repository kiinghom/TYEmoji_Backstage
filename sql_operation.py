from flask_login import login_user, logout_user, current_user, login_required
from flask import Blueprint, g, flash, session
from app import lm, db, app

from app.auth.email import send_email
from app.auth.token import generate_confirmation_token, confirm_token

from app.auth.form import LoginForm, RegisterForm, ChangePasswordForm
from flask import render_template, request, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from PIL import Image

class User(db.Model):
    __tablename__ = 'user'
  	user_email = db.Column(db.String(100),primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(200))

    def __init__(self, name, email, pwd):
        self.user_email = email
        self.userName = name
        self.password = generate_password_hash(pwd)

class User_Image(db.Model):
    __tablename__ = 'user_image'
    image_path = db.Column(db.String(100), primary_key=True)
    image_name = db.Column(db.String(100))
    image_height = db.Column(db.Integer)
    image_width = db.Column(db.Integer)
    public = db.Column(db.Boolean)
    category_name = db.Column(db.String(100))
    user_email = db.Column(db.String(100))

class Category(db.Model):
    __tablename__ = 'category'
    category_name = db.Column(db.String(100),primary_key=True)
    category_cover_path = db.Column(db.String(100))
    category_description = db.Column(db.String(200))
    finished = db.Column(db.Boolean)

class Template_Image(db.Model):
    __tablename__ = 'template_image'
    image_path = db.Column(db.String(100), primary_key=True)
    image_name = db.Column(db.String(100))
    image_height = db.Column(db.Integer)
    image_width = db.Column(db.Integer)
    insert_x = db.Column(db.Integer)
    insert_y = db.Column(db.Integer)
    insert_height = db.Column(db.Integer)
    insert_width = db.Column(db.Integer)

#1.1注册函数 ，参数为邮箱地址，用户名，密码，确认密码
def register_func(email,username,password,confirm):  
    if not username or not email or not password or not confirm:
        flash('UnComplete Input!', 'error')
        return "INPUTERR"
    if confirm != password:
        flash('Confirm Password!', 'error')
        return "PWDERR"
    user=User.query.filter_by(user_email=email).first();
    if user!=None and user.user_email==email:
        print email
        return "REPEAT"
    user = User()
    user.user_email=email
    user.username=username
    user.password=generate_password_hash(password)
    db.session.add(user)
    db.session.commit()
    return "SUCCEED"


#1.2登录函数，参数为邮箱地址，密码
def login_func(email, password):
    user = User.query.filter_by(UserEmail=email).first()
    if user == None:
        return "NOACCOUNT"
    else:
        if check_password_hash(user.password, password):
            return "SUCCEED"
        else:
            return "WRONGPWD"

#2上传图片函数，将base64转为图片，存在服务器上对应私人文件夹，在数据库中插入对应条目
def upload_image(email,finished,image_name,base64code_for_img)：
    if (finished):
        image_path='/root/SEPJIMG/user/'+email+'/finished/'+image_name;
    else:
        image_path='/root/SEPJIMG/user/'+email+'/material/'+image_name;
    temp_img = open(image_path "wb")
    temp_img.write(base64.b64decode(base64code_for_img))
    temp_img.close();
    img = Image.open(image_path)
    pic_width, pic_height= img.size
    user_image=User_Image()
    user_image.image_path=image_path
    user_image.image_name=image_name
    user_image.image_width=pic_width
    user_image.image_height=pic_height
    user_image.public= False
    user_image.user_email = email
    db.session.add(user_image)
    db.session.commit()

#2 下载图片到私人文件夹 
def download_image(email,finished,image_name,download_img_path):
    if (finished):
        image_path='/root/SEPJIMG/user/'+email+'/finished/'+image_name
    else:
        image_path='/root/SEPJIMG/user/'+email+'/material/'+image_name
    f = open(download_img_path,'rb');
    download_code = base64.b64encode(f.read())
    temp_img = open(image_path "wb")
    temp_img.write(base64.b64decode(download_code))
    temp_img.close();
    img = Image.open(image_path)
    pic_width, pic_height= img.size
    user_image=User_Image()
    user_image.image_path=image_path
    user_image.image_name=image_name
    user_image.image_width=pic_width
    user_image.image_height=pic_height
    user_image.public= False
    user_image.user_email = email
    db.session.add(user_image)
    db.session.commit()


#3 发布表情包
def release_emoji(email,image_name,category_name):
    user_image=User_Image.query.filter_by(user_email=email).filter_by(image_name=image_name).first()
    user_image.public=True
    user_image.category_name=category_name
    db.session.commit()

#4 获取类别信息
def get_categories():
    return Category.query().all()

#5.1 获取某类别的第page页图片 （公共）
def get_img_by_category_public(category_name,page):
    return  User_Image.query.filter_by(category_name=category_name).filter_by(public=True).order_by(User_Image.image_name).offset(page*5).limit(5)

#5.2 获取某类别的第page页图片 （用户自身）
#def get_img_by_category_personal(email,category_name,page):
 #   return User_Image.query.filter_by(category_name=category_name).filter_by(user_email=email).order_by(User_Image.image_name).offset(page*5).limit(5)

if __name__ == '__main__':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:SEPJ2017@localhost:3306/SEPJ?charset=utf8'
    db.init_app(app)
    app.run(debug=True)