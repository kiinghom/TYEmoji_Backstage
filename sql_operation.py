# -*- coding: utf-8 -*-
from flask import Flask,jsonify
from werkzeug.security import check_password_hash, generate_password_hash
import os
from PIL import Image
from flask_sqlalchemy import SQLAlchemy
import base64
from app import app,db
import json
from sqlalchemy import desc

#db=SQLAlchemy()
class User(db.Model):
    __tablename__ = 'user'
    user_email = db.Column(db.String(100),primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(200))
    def is_active(self):
        return True
    def get_id(self):
        return self.user_email
    def is_authenticated(self):
        return True
    def is_anonymous(self):
        return False

class User_Image(db.Model):
    __tablename__ = 'user_image'
    image_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    image_path = db.Column(db.String(100))
    image_name = db.Column(db.String(100))
    image_height = db.Column(db.Integer)
    image_width = db.Column(db.Integer)
    public = db.Column(db.Boolean)
    category_name = db.Column(db.String(100))
    user_email = db.Column(db.String(100))
    upvote = db.Column(db.Integer)
    def dump(self):
        return {'image_id': self.image_id,
                'file_id':self.image_id,
                'image_path':self.image_path,
                'image_name': self.image_name,
                'category_name':self.category_name,
                'user_email':self.user_email,
                'public':self.public,
                'like_number':self.upvote,
                'groupid':self.category_name
                }

class Category(db.Model):
    __tablename__ = 'category'
    category_name = db.Column(db.String(100),primary_key=True)
    category_cover_path = db.Column(db.String(100))
    category_description = db.Column(db.String(200))
    finished = db.Column(db.Boolean)
    category_id = db.Column(db.Integer)
    def dump(self):
        return  ({
                'tid':self.category_id,
                'name': self.category_name,
                #'category_description': self.category_description,
                'icon': "http://47.100.30.141:5000/photo/get_image_by_path?image_path="+self.category_cover_path,
                #'finished': self.finished
                })

class Template_Image(db.Model):
    __tablename__ = 'template_image'
    image_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    image_path = db.Column(db.String(100))
    image_name = db.Column(db.String(100))
    image_height = db.Column(db.Integer)
    image_width = db.Column(db.Integer)
    insert_x = db.Column(db.Integer)
    insert_y = db.Column(db.Integer)
    insert_height = db.Column(db.Integer)
    insert_width = db.Column(db.Integer)

class Popular_Image(db.Model):
	__tablename__ = 'popular_img'
	image_id = db.Column(db.Integer,primary_key=True)
	upvote = db.Column(db.Integer)


#1.1注册函数 ，参数为邮箱地址，用户名，密码，确认密码
def register_func(email,username,password,confirm):
    if not username or not email or not password or not confirm:
        return "INPUTERR"
    if confirm != password:
        return "PWDERR"
    user=User.query.filter_by(user_email=email).first()
    if user!=None and user.user_email==email:
        print email
        return "REPEAT"
    user = User()
    user.user_email=email
    user.username=username
    user.password=generate_password_hash(password)
    db.session.add(user)
    db.session.commit()
    os.mkdir('/root/SEPJIMG/user/'+email)
    os.mkdir('/root/SEPJIMG/user/'+email+'/finished')
    os.mkdir('/root/SEPJIMG/user/'+email+'/material')
    return "SUCCEED"

#1.2登录函数，参数为邮箱地址，密码
def login_func(email, password):
    user = User.query.filter_by(user_email=email).first()
    if user == None:
        return None,"NOACCOUNT"
    else:
        if check_password_hash(user.password, password):
            return user,"SUCCEED"
        else:
            return None,"WRONGPWD"

#2上传图片函数，将base64转为图片，存在服务器上对应私人文件夹，在数据库中插入对应条目
def upload_image(email,finished,image_name,base64code_for_img):
    current_id = User_Image.query.count()+1
    if (finished):
        image_path='/root/SEPJIMG/user/'+email+'/finished/'+str(current_id)
    else:
        image_path='/root/SEPJIMG/user/'+email+'/material/'+str(current_id)
    temp_img = open(image_path,"wb")
    temp_img.write(base64.b64decode(base64code_for_img))
    temp_img.close()
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


#2 下载图片到手机
def download_image_to_phone(image_id):
    this_image = User_Image.query.filter_by(image_id=image_id).first()
    return this_image.dump()  

#3 发布表情包
def release_emoji(image_id,category_name):
    user_image=User_Image.query.filter_by(image_id=image_id).first()
    user_image.public=True
    user_image.category_name=category_name
    db.session.commit()

#4 获取类别信息
def get_categories(screen_height,screen_width):
    test = Category.query.all()
    category_array= [o.dump() for o in test]
    for i in range(len(category_array)):
        category_array[i]['icon'] = category_array[i]['icon'] + "&screen_height="+str(screen_height)+"&screen_width="+str(screen_width)
        category_array[i]['url']='http://47.100.30.141:5000/photo/get_img_by_category_public?category_name='+category_array[i]['name']+"&screen_height="+str(screen_height)+"&screen_width="+str(screen_width)
    return json.dumps(category_array)

#5.1 获取某类别的第page页图片 （公共）
def get_img_by_category_public(category_name,screen_height,screen_width,page):
    this_category_id=Category.query.filter_by(category_name=category_name).first().category_id
    print this_category_id
    test = User_Image.query.filter_by(category_name=category_name).filter_by(public=True).order_by(User_Image.image_name).offset(page*5).limit(5).all()
    image_array = [o.dump() for o in test]  
    for i in range(len(image_array)):
        image={"small":'http://47.100.30.141:5000/photo/get_image_by_path?image_path='+image_array[i]['image_path']+"&screen_height="+str(screen_height/3)+"&screen_width="+str(screen_width/3),
                'original':'http://47.100.30.141:5000/photo/get_image_by_path?image_path='+image_array[i]['image_path']+"&screen_height="+str(screen_height)+"&screen_width="+str(screen_width)}
        #image_array[i]['image']['small']='http://47.100.30.141:5000/photo/get_image_by_path?image_path='+image_array[i]['image_path']+"&screen_height="+str(screen_height/3)+"&screen_width="+str(screen_width/3)
        #image_array[i]['image']['big']='http://47.100.30.141:5000/photo/get_image_by_path?image_path='+image_array[i]['image_path']+"&screen_height="+str(screen_height)+"&screen_width="+str(screen_width)
        image_array[i]['image']=image
        image_array[i]['groupid']=this_category_id
    #return json.dumps([o.dump() for o in test])
    #return json.dumps(image_array)
    return image_array

#5.2获取用户图片
def get_img_by_user(email,screen_height,screen_width,page):
    test = User_Image.query.filter_by(user_email=email).order_by(User_Image.image_name).offset(page*5).limit(5).all() 
    image_array = [o.dump() for o in test]
    for i in range(len(image_array)):
        image={"small":'http://47.100.30.141:5000/photo/get_image_by_path?image_path='+image_array[i]['image_path']+"&screen_height="+str(screen_height/3)+"&screen_width="+str(screen_width/3),
                'original':'http://47.100.30.141:5000/photo/get_image_by_path?image_path='+image_array[i]['image_path']+"&screen_height="+str(screen_height)+"&screen_width="+str(screen_width)}
        image_array[i]['image']=image
    return image_array
    #return json.dumps([o.dump() for o in test])

#获取点赞数最多的图片
def get_img_by_upvote(screen_height,screen_width,page):
    test = User_Image.query.filter_by(public=True).order_by(desc(User_Image.upvote)).offset(page*5).limit(5).all() 
    image_array = [o.dump() for o in test]
    for i in range(len(image_array)):
        image={"small":'http://47.100.30.141:5000/photo/get_image_by_path?image_path='+image_array[i]['image_path']+"&screen_height="+str(screen_height/3)+"&screen_width="+str(screen_width/3),
                'original':'http://47.100.30.141:5000/photo/get_image_by_path?image_path='+image_array[i]['image_path']+"&screen_height="+str(screen_height)+"&screen_width="+str(screen_width)}
        image_array[i]['image']=image
    return image_array

#6获取热门图片
def get_popular_img(page):
    test = Popular_Image.query.order_by(desc(Popular_Image.upvote)).offset(page*5).limit(5).all()
    arr=[]
    for each in test:
        this_image = User_Image.query.filter_by(image_id=each.image_id).first()
        this_popular_img = this_image.dump()
        this_popular_img['upvote']=each.upvote
        arr.append(this_popular_img)
    return arr


#7点赞
def upvote(image_id):
    popular_img=Popular_Image.query.filter_by(image_id=image_id).first()
    popular_img.upvote=popular_img.upvote+1;
    db.session.commit()
	
#app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:SEPJ2017@localhost:3306/SEPJ?charset=utf8'
#db.init_app(app)
#ctx = app.app_context()
#ctx.push() 
#test case
#print '1',register_func('163@163.com','ljh','test','test')
#print '1.1',login_func('163@163.com','test');
#print '2',download_image_to_phone(3)
#print '3',release_emoji(5,'happy');
#print '3',release_emoji(6,'happy');
#print '3',release_emoji(7,'happy');
#print '3',release_emoji(8,'happy');
#print '3',release_emoji(9,'happy');
#print '4',get_categories()
#print '5',get_img_by_category_public('happy',1)
	
#app.run(debug=True)
