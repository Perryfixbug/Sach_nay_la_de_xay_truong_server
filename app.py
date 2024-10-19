import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_session import Session
from datetime import timedelta
from sqlalchemy import create_engine, text

# Import các module khác của bạn
from db import db
from cart_option import CartOption
from user_option import User_option 
from product_option import Prod
from bill_option import Bill_Option 
from route.home import home
from route.product_route import product_route
from route.cart_route import cart_route
from route.account_route import acc_route
from route.image_route import image_r
from route.bill_route import bill_route

def create_app():
    app = Flask(__name__)
    
    # Đường dẫn cơ sở dữ liệu SQLite
    db_path = os.path.join(os.path.dirname(__file__), 'user (1).db')  # Sử dụng tên file chính xác
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    # Khởi tạo engine cho SQLAlchemy
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    
    # Cấu hình session
    app.config['SECRET_KEY'] = 'your_secret_key_here'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)
    app.config['SESSION_COOKIE_SECURE'] = False  # Đặt là True nếu bạn sử dụng HTTPS
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'None'

    # Khởi tạo Flask-Session
    Session(app)
    
    # Đăng ký các Blueprints
    app.config['Prod'] = Prod(db=db)
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
        db.create_all()  # Tạo tất cả bảng
