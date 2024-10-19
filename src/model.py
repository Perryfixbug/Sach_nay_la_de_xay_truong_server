from db import db
from sqlalchemy import Integer, String, Column, Float, Boolean, ForeignKey, BINARY
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta

class Product(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    img = Column(String(100), default='product_default')
    price = Column(String(30), nullable=False)
    author = Column(String(50), nullable=False)
    detail = Column(String(200), nullable=True)
    category = Column(String(50), nullable=False)
    stock = Column(Integer, default=1)
    isPopular = Column(Boolean, default=False)
    pcarts = relationship('PCart', back_populates='product', lazy=True)
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'img': self.img,
            'price': self.price,
            'author': self.author,
            'detail': self.detail,
            'category': self.category,
            'stock': self.stock,
            'isPopular': self.isPopular
        }

class PCart(db.Model):
    id = Column(Integer, primary_key=True, autoincrement= True)
    u_id = Column(Integer, nullable= False)
    p_id = Column(Integer, ForeignKey('product.id'), nullable= False)
    date = Column(String(20), default=str(datetime.today().date()))
    quantity = Column(Integer, default=1)
    product = relationship('Product', back_populates='pcarts', lazy=True)
    def to_dict(self):
        if self.product:
            product_info = self.product
            return {
                'id': self.p_id,
                'name': product_info.name,
                'img': product_info.img,
                'price': product_info.price,
                'author': product_info.author,
                'date': self.date,
                'detail': product_info.detail,
                'category': product_info.category,
                'quantity': self.quantity
            }
        return {}

class User(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(BINARY, nullable=False)
    email = Column(String(50), nullable=True)
    phone = Column(String(50), nullable=True)
    img = Column(String(100), default='user_default.jpg')
    point = Column(Integer, nullable=False, default=0)
    birthday = Column(String(20), default='None')
    gender = Column(String(10), default='None')
    purchased = Column(Integer, nullable=False, default=0)
    donations = Column(Integer, nullable=False, default=0)
    locate = Column(String(100), nullable=True)
    role = Column(Integer, nullable=False, default=0)  # 0 is user, 1 is admin
    def rank(self):
        if self.point > 5000:
            return "Kim Cuong"
        elif self.point > 3000: 
            return "Gold"
        elif self.point > 2000:
            return "Silver"
        elif self.point > 1000:
            return "Bronze"
        else:
            return "NewUser"
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'phone': self.phone,
            'img': self.img,
            'point': self.point,
            'birthday': self.birthday,
            'gender': self.gender,
            'purchased': self.purchased,
            'donations': self.donations,
            'role': self.role
        }

class Bill(db.Model):  
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable= False)
    orders = Column(String(300), nullable=False)
    orderdate = Column(String(20), default=str(datetime.today().date()))
    method = Column(String(20), default='COD') 
    status = Column(Integer, default=0)  # 0: not received, 1: received, 2: overdue
    recipient = Column(String(100))
    address = Column(String(100))
    phone = Column(String(20))
    total_price = Column(Integer, nullable=False)
    
    def to_dict(self):
        return {
           'id' : self.id,
           'orders': self.orders,
           'orderdate' : self.orderdate,
           'method' : self.method,
           'status': self.status,
           'recipient': self.recipient,
           'address'  : self.address,
           'phone'  : self.phone,
           'total_price': self.total_price
        }
