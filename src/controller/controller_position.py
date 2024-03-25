import time

from flask import Blueprint
from flask import request
from flask_cors import cross_origin

from service.exness_order import get_all_positions
from service.exness_order import get_position
from service.exness_order import close_position
from service.exness_order import close_position_by_volume

URL_PREFIX = '/api/v1/exness'
bp = Blueprint('positions', __name__, url_prefix=URL_PREFIX)


@bp.route('/positions', methods=['GET'])
@cross_origin()
def exness_all_positions():
    ticket = request.args.get('ticket', type=int)
    if ticket is not None:
        res, code, msg = get_position(ticket)
        if res is None:
            return msg, 404
        return {
            "code": code,
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
            "msg": msg,
            "data": res
        }, 200
    else:
        symbol = request.args.get('symbol', type=str, default='BTCUSD')
        res, code, msg = get_all_positions(symbol=symbol)
        if res is None:
            return msg, 404
        return {
            "code": code,
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
            "msg": msg,
            "data": res
        }, 200


@bp.route('/positions', methods=['PUT'])
@cross_origin()
def exness_close_position_by_volume():
    payload = request.get_json()
    ticket = int(payload['ticket'])
    volume = float(payload['volume'])
    res, code, msg = close_position_by_volume(ticket=ticket, volume=volume)
    if res is None:
        return msg, 404
    else:   
        return {
            "code": code,
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
            "msg": msg,
            "data": res
        }, 200


@bp.route('/positions', methods=['DELETE'])
@cross_origin()
def exness_close_position():
    payload = request.get_json()
    ticket = int(payload['ticket'])
    res, code, msg = close_position(ticket)
    if res is None:
        return msg, 404
    return {
        "code": code,
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
        "msg": msg,
        "data": res
    }, 200

