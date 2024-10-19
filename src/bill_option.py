from flask import jsonify, request,session
from model import Bill, Product
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import re

class Bill_Option:
    def __init__(self, db: SQLAlchemy):
        self.db = db
        self.status = 4
        self.user = 0
    def get_user(self):
        if not session.get('uid'):
            self.user = 0
        else: self.user = str(session['uid'])
        print(self.user)
    def get_bill(self):
        try:
            orlist = Bill.query.all()
            if not len(orlist):
                return jsonify('Không tìm thấy đơn hàng nào theo yêu cầu'), 404
            return jsonify([o.to_dict() for o in orlist])
        except Exception as e:
            return jsonify("error" + str(e)), 500
    def add_bill(self):
        try:
            # if not self.user:
            #     return jsonify("Ban khong the thanh toan neu khong dang nhap"), 404
            data = request.get_json()
            if not data:
                return jsonify("Dữ liệu không hợp lệ"), 400

            # Kiểm tra các trường bắt buộc
            if not data.get('phone'):
                return jsonify(" Bạn cần cung cấp thêm số điện thoại"), 400
            if not data.get('address'):
                return jsonify(" Bạn cần cung cấp thêm địa chỉ nhận hàng"), 400
            if not data.get('recipient'):
                return jsonify(" Bạn thiếu tên người nhận hàng"), 400

            # Kiểm tra danh sách sản phẩm (orders)
            if not data.get('orders'):
                return jsonify({"Danh sách sản phẩm không được để trống"}), 400
            if not data.get("payment_method"):
                data["payment_method"] = 'COD'
            
            # Tạo đối tượng Bill
            bill = Bill(
                recipient=data['recipient'],
                phone=data['phone'],
                address=data['address'],
                orders=data['orders'], 
                total_price=int(data['total_price']),
                method = data["payment_method"],
                user_id=self.user  # Sử dụng user_id từ phiên đăng nhập
            )

            # Lưu vào cơ sở dữ liệu
            self.db.session.add(bill)
            self.db.session.commit()

            # Trả về phản hồi thành công
            return jsonify(" Đã thêm một đơn hàng mới!"), 200

        except Exception as e:
            # Xử lý lỗi và trả về thông báo lỗi
            return jsonify("error "+ str(e)), 500
