from flask import Blueprint, request

URL_PREFIX = '/api/v1/exness'
bp = Blueprint('account', __name__, url_prefix=URL_PREFIX)


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
