from flask import Blueprint, request
from flask_cors import cross_origin

from service.exness_withdraw import withdraw as exness_withdraw
from service.exness_withdraw import get_binance_withdrwal_address

import logging
import json
from datetime import datetime

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s|%(name)s|%(levelname)s|%(message)s')

URL_PREFIX = '/api/v1/exness'
bp = Blueprint('withdraw', __name__, url_prefix=URL_PREFIX)

@bp.route('/withdraw', methods=['POST'])
@cross_origin()
def withdraw():
    logging.info(f"POST|{URL_PREFIX}/withdraw|payload:[{request.get_data(as_text=True)}]")
    payload = request.get_json()
    network = payload['network']
    amount = float(payload['amount'])
    res = exness_withdraw(network=network, amount=amount)
    return res, 200

@bp.route('/withdraw/address', methods=['GET'])
@cross_origin()
def address():
    logging.info(f"GET|{URL_PREFIX}/withdraw/address")
    network = request.args.get('network', type=str, default='')
    res = get_binance_withdrwal_address(network=network)
    return res, 200 