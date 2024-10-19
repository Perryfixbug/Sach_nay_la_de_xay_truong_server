from flask import jsonify, request, session
from model import PCart
from flask_sqlalchemy import SQLAlchemy

class CartOption:
    def __init__(self, db: SQLAlchemy, engine) -> None:
        self.db = db
        self.engine = engine
        self.userlogin = 0
        self.usercart = []
        
    def get_usercart(self, u_id = None):
        # Nếu có uid trong session, lấy giỏ hàng của người dùng
        print(session)
        if session.get('uid'):
            self.userlogin = int(session['uid'])
            print(self.userlogin)
            self.usercart = PCart.query.filter(PCart.u_id == self.userlogin)
            print(f'Đã thêm người dùng {session["uid"]}')

        else:
            print("Gio hang khach")
            # Nếu không có uid, giỏ hàng sẽ là một danh sách trống
            self.usercart = PCart.query.filter(PCart.u_id == 0)  

    def get_Cart(self, p_id=None):
        try:       
            if not self.userlogin:
                self.get_usercart(self.userlogin)
            #     return jsonify([]), 200  # Trả về giỏ hàng trống

            pc = self.usercart
            if p_id:
                pc = pc.filter(PCart.id == p_id)
            products = pc.all()
            return jsonify([p.to_dict() for p in products]), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def add_Cart(self, product_id=None):
        try:
            # Nếu giỏ hàng trống và không có uid, không yêu cầu đăng nhập
            # if not self.userlogin:
            #     return jsonify('Cần đăng nhập để thêm vào giỏ hàng'),400
            if not product_id:
                data = request.get_json()
                if not data or 'productId' not in data:
                    return jsonify({"error": "Invalid input"}), 400
                product_id = data['productId']
            pc = PCart.query.filter(PCart.p_id == product_id, PCart.u_id == self.userlogin).first()
            if not pc:
                pc = PCart(p_id=product_id, u_id=self.userlogin)
                self.db.session.add(pc)
            else:
                pc.quantity += 1
            self.db.session.commit()
            return jsonify(self.usercart.count()), 200
        except Exception as e:
            self.db.session.rollback()
            return jsonify({"error": str(e)}), 500

    def delete_Cart(self, product_id=None):
        try:
            # if not self.userlogin:
            #     return jsonify('Giỏ hàng trống. Bạn không thể xóa sản phẩm khi chưa đăng nhập.'), 400
            
            if not product_id:
                data = request.get_json()
                if not data or 'product_id' not in data:
                    return jsonify({"error": "Invalid input"}), 400
                product_id = data['product_id']

            item =  PCart.query.filter(PCart.p_id == product_id, PCart.u_id == self.userlogin).first()
            if item:
                self.db.session.delete(item)
                self.db.session.commit()
                return jsonify(self.usercart.count()), 200
            else:
                return jsonify({"error": "Sản phẩm không có trong Giỏ hàng"}), 404
        except Exception as e:
            self.db.session.rollback()
            return jsonify({"error": str(e)}), 500
    def delete_guest_cart(self):
        try:
            if not self.userlogin:
                PCart.query.filter(PCart.u_id == 0).delete()
                self.db.session.commit()
                print("Đã xóa giỏ hàng của khách.")
        except Exception as e:
            self.db.session.rollback()
            return jsonify({"error": str(e)}), 500