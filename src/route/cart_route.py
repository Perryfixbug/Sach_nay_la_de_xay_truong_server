from flask import request, jsonify, Blueprint, current_app,session

cart_route = Blueprint('cart_route', __name__)

@cart_route.route('/cart', defaults={'product_id': None}, methods=['GET', 'POST', 'DELETE'])
@cart_route.route('/cart/<int:product_id>', methods=['DELETE'])
def Cartpage(product_id):
    if session.get('uid') is None:
        current_app.config['AccOption'].create_guest()
    current_app.config['cartOption'].get_usercart()
    if request.method == 'GET':
        return current_app.config['cartOption'].get_Cart()
    if request.method == 'POST':
        return current_app.config['cartOption'].add_Cart()
    
    if request.method == 'DELETE':
        return current_app.config['cartOption'].delete_Cart(product_id=product_id)
