from db import db
from model import Product
from flask import jsonify, request
from flask_sqlalchemy import SQLAlchemy
from image_path import save_image
from datetime import datetime 


class Prod:
    def __init__(self, db: SQLAlchemy) -> None:
        self.db = db
    def sell_product(self):
        data = request.get_json()
        order = {}
        order['method_pay'] = data['method_pay']
        order['p_id'] = data['p_id']
        order['u_id'] = data['u_id']
        order['date'] = datetime.today().date()
        return jsonify(order)
    
    def get_Prod(self, prod_id=None):
        gp = Product.query
        if prod_id:
            gp = gp.filter(Product.id.__eq__(prod_id)).first() 
            if gp:
                return jsonify(gp.to_dict())
            else:
                return jsonify({'error': 'Product not found'}), 404
        products = gp.all()
        return jsonify([p.to_dict() for p in products])

    def add_Prod(self):
        name = request.form.get('name')
        price = request.form.get('price')
        author = request.form.get('author')
        detail = request.form.get('detail')
        category = request.form.get('category')
        stock = request.form.get('stock')
        
        file = request.files.get('file')
        find_img,mes = save_image(file,'product')
        if not find_img:
            return jsonify(mes)
        new_product = Product(
            name=name,
            price=int(price),
            author=author,
            detail=detail,
            category=category,
            stock=int(stock),
            image=mes  
        )
        try:
            db.session.add(new_product)
            db.session.commit()
            return f"Product '{name}' has been added successfully."
        except Exception as e:
            db.session.rollback() 
            return f"An error occurred while adding the product: {str(e)}"
        