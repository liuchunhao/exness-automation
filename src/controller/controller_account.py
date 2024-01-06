from flask import Blueprint, request

bp = Blueprint('account', __name__, url_prefix='/account')


@bp.route('/positions', methods=['GET'])
def position_list():
    data = request.get_json()
    # TODO: get position list
    return 'Received the GET request', 200


@bp.route('/orders', methods=['GET'])
def order_list():
    data = request.get_json()
    # TODO: get order list
    return 'Received the GET request', 200  


@bp.route('/balance', methods=['GET'])
def balance():
    data = request.get_json()
    # TODO: get balance
    return 'Received the GET request', 200
