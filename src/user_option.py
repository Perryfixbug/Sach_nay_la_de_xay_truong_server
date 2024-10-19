from flask import jsonify, request, session
from model import User
from flask_sqlalchemy import SQLAlchemy
from image_path import save_image
from sqlalchemy import Integer, String, Column, ForeignKey, text, inspect
from datetime import datetime, timedelta
import bcrypt
import re

def validate_email_phone(email_phone):
    email, phone = None, None
    # Biểu thức chính quy cho email
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    
    # Biểu thức chính quy cho số điện thoại (chấp nhận số bắt đầu bằng + hoặc không)
    phone_regex = r'^\+?\d{10,15}$'
    if re.match(email_regex, email_phone):
        email = email_phone
    # Kiểm tra xem chuỗi có phải là số điện thoại không
    elif re.match(phone_regex, email_phone):
        phone = email_phone

    return email, phone

class User_option:
    def __init__(self, db: SQLAlchemy, engine) -> None:
        self.db = db
        self.engine = engine
    def add_user(self): 
        try:
            data = request.get_json() 
            if not data:
                return jsonify("Invalid input"), 400
            username = data['username']
            password = data['password'] 
            email_phone= data['email_phone']
            re_password = data['repass']

            if not username or not password or not email_phone or not re_password:
                return jsonify("Cần nhập đầy đủ thông tin."), 400
            
            email,phone = validate_email_phone(email_phone=email_phone)
            if not email and not phone :
                return jsonify('Hãy đảm bảo đúng định dạng email hoặc số điện thoại'), 400
            
            existing_user = None
            if email:
                existing_user = User.query.filter((User.email == email)).first()
            elif phone:
                existing_user = User.query.filter((User.phone == phone)).first()
            if existing_user:
                return jsonify('Email hoặc số điện thoại này đã đăng ký cho một tài khoản khác'), 400
            existing_user = User.query.filter((User.username == username)).first()
            if existing_user:
                return jsonify('Tên đăng nhập bạn sử dụng đã trùng với tên của người khác'), 400
            
            if len(password) < 8: 
                return jsonify('Mật khẩu phải có tối thiểu 8 ký tự'), 400
            
            has_letter = re.search(r'[a-zA-Z]', password) is not None
            has_digit = re.search(r'\d', password) is not None
            if not (has_letter and has_digit):
                return jsonify('Mật khẩu phải bao gồm cả chữ cái và chữ số'), 400
            
            if re_password != password:
                return jsonify("Mật khẩu không giống nhau"), 400

            # Băm mật khẩu
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            # Tạo một đối tượng User
            user = User(
                username=username,
                password=hashed_password,  # Lưu mật khẩu đã băm ở dạng bytes
                img='default_user.jpg',  # Hình ảnh mặc định
                email = email,
                phone = phone
            )
            self.db.session.add(user)
            self.db.session.commit()
            return jsonify("message: Đã tạo tài khoản mới thành công"), 201  # Trả về mã 201 khi tạo thành công

        except Exception as e:
            self.db.session.rollback()  
            return jsonify(" " + str(e)), 500  # Trả về lỗi nếu có

    def delete_user(self):
        data = request.get_json()
        if not data: 
            return jsonify("Invalid input"), 400
        user = User.query.get(data['id'])
        if user:
            self.db.session.delete(user)
            self.db.session.commit()
            return jsonify("Đã xóa tài khoản của bạn!"), 200
        else:
            return jsonify("Người dùng không tồn tại"), 404
        
    def login(self):
        try:
            data = request.get_json()
            if not data:
                return "Invalid input", 400
            password = data['password'] 
            email = data['email']
            user = User.query.filter((User.email.__eq__(email))| (User.phone.__eq__(email))).first()
        except Exception as e:
            return " " + str(e), 500  # Trả về lỗi nếu có
        if not user:
            return "Tên tài khoản không tồn tại", 404
        
        # Kiểm tra mật khẩu
        if not bcrypt.checkpw(password.encode('utf-8'), user.password): 
            return "Mật khẩu không chính xác", 401
        
        return str(user.id), 200

    def update_user(self):
        try:
            data = request.get_json()
            if not data:
                return jsonify("Invalid input"), 400
            user = User.query.get(data.get('id'))

            # Cập nhật các trường khác
            if data.get('username'):
                user.username = data['username']
            if data.get('birthday'):
                user.birthday = data['birthday']
            if data.get('gender'):
                user.gender = data['gender']
            if data.get('email'):
                user.email = data['email']
            if data.get('phone'):
                user.phone = data['phone']
            if data.get('password'):
                user.password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            # Lấy ảnh đại diện từ request
            if 'img' in request.files:
                avt = request.files['img']
                success, result = save_image(file=avt, endpoint="user_avt")
                if success:
                    user.img = avt.filename  
                else:
                    return jsonify(result),401

            # Lưu các thay đổi vào cơ sở dữ liệu
            self.db.session.commit()
            return jsonify("Người dùng đã được cập nhập thông tin"), 200
        except Exception as e:
            self.db.session.rollback()
            return jsonify(str(e)), 500
        
    def profile(self, user_id=None):
        if not user_id:
            return jsonify("Hãy chỉ rõ người dùng"), 404
        user = User.query.get(user_id)
        if not user:
            return jsonify("Không tìm thấy người dùng")
        return jsonify(user.to_dict()), 200  # Trả về thông tin người dùng

    def logout(self):
        session.pop('user_id', None)  # Xóa user_id khỏi session
        return jsonify("Đăng xuất thành công"), 200
    def create_guest(self):
        user = User.query.get(0)
        if user:
            self.db.session.delete(user)
            self.db.session.commit() 
        user = User(
            id = 0,
            username = 'Guest',
            password =  bcrypt.hashpw('Taikhoankhach'.encode('utf-8'), bcrypt.gensalt()),
            img='default_user.jpg',  # Hình ảnh mặc định
            email = '',
            phone = ''
        )
        self.db.session.add(user)
        self.db.session.commit()

