from flask import request, jsonify, Blueprint, current_app,session

bill_route = Blueprint('bill_route', __name__)

@bill_route.route('/bill', methods=['GET', 'POST'])
def billpage():
    #current_app.config['billOption'].get_user()
    if request.method == 'GET':
        return current_app.config['billOption'].get_bill()
    if request.method == 'POST':
        return current_app.config['billOption'].add_bill()
