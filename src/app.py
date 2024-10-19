from flask import Flask, jsonify, url_for,request,session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from flask_cors import CORS
from cart_option import CartOption
from user_option import User_option 
from product_option import Prod
from bill_option import Bill_Option
from datetime import timedelta
from flask_session import Session
from db import db
from route.home import home
from route.product_route import product_route
from route.cart_route import cart_route
from route.account_route import acc_route
from route.image_route import image_r
from route.bill_route import bill_route
from os import path

def create_app():
    app = Flask(__name__)
    #Database
    app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///user (1).db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    engine = create_engine('sqlite:///user (1).db')
    # Cấu hình session
    app.config['SECRET_KEY'] = '8SIAs98h9sd9198gs*^G^@hs'  # Key bí mật
    app.config['SESSION_TYPE'] = 'filesystem'  # Hoặc 'redis', 'memcached', v.v.
    app.config['SESSION_PERMANENT'] = True  # Không lưu session vĩnh viễn
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)  # Thời gian sống của session
    # Cấu hình session cookie
    app.config['SESSION_COOKIE_SECURE'] = True   # Nếu không dùng HTTPS, hãy để False
    app.config['SESSION_COOKIE_HTTPONLY'] = True  # Chỉ cho phép truy cập session qua HTTP, không qua JavaScript
    app.config['SESSION_COOKIE_SAMESITE'] = 'None'  # Cấu hình chính sách cross-site
    app.config['SESSION_UID'] = 0
    Session(app)  # Khởi tạo session
    #Dang ky cac BluePrint
    app.config['Prod'] = Prod(db = db)
    app.config['cartOption'] = CartOption(db=db, engine=engine)
    app.config['AccOption'] = User_option(db=db, engine=engine)
    app.config['billOption'] = Bill_Option(db=db)
    app.register_blueprint(product_route)
    app.register_blueprint(cart_route)
    app.register_blueprint(home)
    app.register_blueprint(acc_route)
    app.register_blueprint(image_r)
    app.register_blueprint(bill_route)
 
    return app
def drop_tables(db: SQLAlchemy):
    tables_to_drop = ['p_cart_1', 'p_cart_2', 'p_cart_3', 'p_cart_4', 'p_cart_5', 'p_cart_6']
    
    with db.engine.connect() as connection:
        for table in tables_to_drop:
            try:
                connection.execute(text(f"DROP TABLE IF EXISTS {table}"))
                print(f"Bảng {table} đã được xóa.")
            except Exception as e:
                print(f"Lỗi khi xóa bảng {table}: {str(e)}")
if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
        app.config['cartOption'].delete_guest_cart()
    CORS(app, supports_credentials=True)
    app.run(debug= True, port= 5000)