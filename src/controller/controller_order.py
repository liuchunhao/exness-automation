import time

from flask import Blueprint, request
from flask_cors import cross_origin

from service.exness_order import market_order
from service.exness_order import limit_order
from service.exness_order import get_order_by_ticket
from service.exness_order import modify_order_by_price
from service.exness_order import get_orders
from service.exness_order import delete_order

URL_PREFIX = '/api/v1/exness'
bp = Blueprint('order', __name__, url_prefix=URL_PREFIX)


@bp.route('/order', methods=['GET']) 
@cross_origin()
def exness_get_order():
    ticket = request.args.get('ticket', type=int, default=None)
    if ticket is None:
        return 'Missing ticket', 400

    ticket = int(ticket)
    res, code, msg = get_order_by_ticket(ticket=ticket)
    if res is None:
        return msg, 404
    return {
        "code": code,
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
        "msg": msg,
        "data": res
    }, 200


@bp.route('/order/list', methods=['GET'])
@cross_origin()
def exness_get_orders_by_symbol():
    symbol = request.args.get('symbol', type=str, default='BTCUSD') 
    res, code, msg = get_orders(symbol=symbol)
    if res is None:
        return msg, 404
    return {
        "code": code,
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
        "msg": msg,
        "data": res
    }, 200


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
    res, code, msg = limit_order(symbol=symbol, order_type=order_type, volume=volume, price=price)
    if res is None:
        return msg, 404

    return {
        "code": code,
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
        "msg": msg,
        "data": res
    }, 200


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
    res, code, msg = market_order(symbol=symbol, order_type=order_type, volume=volume)
    if res is None:
        return msg, 404
    return {
        "code": code,
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
        "msg": msg,
        "data": res
    }, 200


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
    res, code, msg = delete_order(ticket=ticket)
    if res is None:
        return msg, 404
    return {
        "code": code,
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
        "msg": msg,
        "data": res
    }, 200


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
    res, code, msg = modify_order_by_price(ticket=ticket, price=price)
    if res is None:
        return msg, 404
    return {
        "code": code,
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
        "msg": msg,
        "data": res
    }, 200

