from flask import Blueprint, request

from auto_withdraw import withdraw as exness_withdraw

import logging
import json
from datetime import datetime

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s|%(name)s|%(levelname)s|%(message)s')

URL_PREFIX = '/api/v1/exness'
bp = Blueprint('exness', __name__, url_prefix=URL_PREFIX)

@bp.route('/withdraw', methods=['POST'])
def withdraw():
    logging.info(f"POST|{URL_PREFIX}/withdraw|payload:[{request.get_data(as_text=True)}]")
    payload = request.get_data(as_text=True) #.replace('\r', '').replace('\n', '').strip()
    body = json.loads(payload)

    # network = body['network']
    # address = body['address']
    amount = int(body['amount'])

    # TODO: 
    # exness_withdraw(network=data['network'], address=data['address'], amount=data['amount'])
    res = exness_withdraw(amount=amount)
    return res

