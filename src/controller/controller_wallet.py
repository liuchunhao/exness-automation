from flask import Blueprint, request
from flask_cors import cross_origin

from service.exness_wallet import get_spot_wallet_list
from service.exness_wallet import transfer

import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s|%(name)s|%(levelname)s|%(message)s')

URL_PREFIX = '/api/v1/exness'
bp = Blueprint('wallets', __name__, url_prefix=URL_PREFIX)

@bp.route('/wallets', methods=['GET'])
@cross_origin()
def exness_spot_wallet_list():
    logging.info(f"GET|{URL_PREFIX}/wallets")
    res = get_spot_wallet_list()
    return res, 200

@bp.route('/wallets/transfer', methods=['POST'])
@cross_origin()
def exness_transfer():
    logging.info(f"POST|{URL_PREFIX}/wallets/transfer|payload:[{request.get_json()}]")  
    payload = request.get_json()
    amount = float(payload['amount'])
    destination = payload['destination']
    wallet = payload['wallet']
    res = transfer(amount=amount, destination=destination, wallet=wallet)
    return res, 200
