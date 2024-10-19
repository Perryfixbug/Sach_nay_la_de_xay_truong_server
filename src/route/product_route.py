from flask import request, jsonify, Blueprint, current_app


product_route = Blueprint('product_route', __name__)

@product_route.route('/product', methods=['GET', 'POST', 'DELETE'])
def Prod():
    return current_app.config['Prod'].get_Prod()

@product_route.route('/product/<product_id>', methods=['GET', 'POST', 'DELETE'])
def prod(product_id = 0):
    if request.method == 'GET':
        return current_app.config['Prod'].get_Prod(prod_id = product_id)