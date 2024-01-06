from flask import Blueprint, request

bp = Blueprint('order_controller', __name__)


@bp.route('/order', methods=['POST']) 
def create_order():
    '''
    {
        "event": "order",
        "type": "3",
        "ticket": "123456789",
    }
    '''
    data = request.get_json()
    # TODO: create order
    return 'Received the POST request', 200


@bp.route('/order', methods=['DELETE'])
def delete_order():
    '''
    {
        "event": "order",
        "type": "3",
        "ticket": "123456789",
    }
    '''
    data = request.get_json()
    # TODO: delete order
    return 'Received the DELETE request', 200


@bp.route('/order', methods=['PUT'])
def modify_order():
    '''
    {
        "event": "order",
        "type": "3",
        "ticket": "123456789",
    }
    '''
    data = request.get_json()
    # TODO: modify order
    return 'Received the MODIFY request', 200
