from flask import Blueprint, request
from flask_cors import cross_origin

from service.exness_order import market_order
from service.exness_order import limit_order
from service.exness_order import get_order_by_ticket
from service.exness_order import modify_order_by_price
from service.exness_order import get_orders
from service.exness_order import delete_order

URL_PREFIX = '/api/v1/exness'
bp = Blueprint('order_controller', __name__, url_prefix=URL_PREFIX)


@bp.route('/order', methods=['GET']) 
@cross_origin()
def exness_get_order():
    ticket = request.args.get('ticket', type=int, default=None)
    if ticket is None:
        return 'Missing ticket', 400

    ticket = int(ticket)
    res = get_order_by_ticket(ticket=ticket)
    '''
    ticket=47247319, 
    time_setup=1710822767, 
    time_setup_msc=1710822767092, 
    time_done=0, 
    time_done_msc=0, 
    time_expiration=0, 
    type=2, 
    type_time=0, 
    type_filling=2, 
    state=1, 
    magic=100, 
    position_id=0, 
    position_by_id=0, 
    reason=3, 
    volume_initial=0.03, 
    volume_current=0.03, 
    price_open=59000.0, 
    sl=0.0, 
    tp=0.0, 
    price_current=62988.01, 
    price_stoplimit=0.0, 
    symbol='BTCUSD', 
    comment='limit order', 
    external_id=''
    '''
    return res, 200


@bp.route('/order/list', methods=['GET'])
@cross_origin()
def exness_get_orders_by_symbol():
    symbol = request.args.get('symbol', type=str, default='BTCUSD') 
    res = get_orders(symbol=symbol)
    if res is None:
        return 'No orders found', 404
    return res, 200


@bp.route('/order/limit', methods=['POST']) 
@cross_origin()
def exness_limit_order():
    # TODO: create limit order
    '''"
    {
        "symbol": "BTCUSD",
        "order_type": "buy",
        "volume": 0.01,
        "price": 60000
    }
    '''
    data = request.get_json()
    symbol = data['symbol']
    order_type = data['order_type']
    volume = float(data['volume'])
    price = float(data['price'])
    res = limit_order(symbol=symbol, order_type=order_type, volume=volume, price=price)
    if res is None:
        return 'Order not created', 404
    return res, 200


@bp.route('/order/market', methods=['POST']) 
@cross_origin()
def exness_market_order():
    # TODO: create market order
    '''
    {
        "symbol": "BTCUSD",
        "order_type": "buy",
        "volume": 0.01
    }
    '''
    data = request.get_json()
    symbol = data['symbol']
    order_type = data['order_type']
    volume = float(data['volume'])
    res = market_order(symbol=symbol, order_type=order_type, volume=volume)
    if res is None:
        return 'Order not created', 404
    return res, 200


@bp.route('/order', methods=['DELETE'])
def exness_delete_order():
    # TODO: delete order
    '''
    {
        "ticket": 123456789,
    }
    '''
    data = request.get_json()
    ticket = int(data['ticket'])
    res = delete_order(ticket=ticket)
    if res is None:
        return 'Order not found', 404
    return res, 200


@bp.route('/order', methods=['PUT'])
def exness_modify_order():
    # TODO: modify order
    '''
    {
        "ticket": 123456789,
        "price": 123.45
    }
    '''
    data = request.get_json()
    ticket = int(data['ticket'])
    price = float(data['price'])
    res = modify_order_by_price(ticket=ticket, price=price)
    if res is None:
        return 'Order not found', 404
    return res, 200

