from flask import Blueprint, request
from flask_cors import cross_origin

from service.exness_transaction_history import list_transaction_history
from service.exness_transaction_history import get_latest_transaction_history

import logging
import json
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s|%(name)s|%(levelname)s|%(message)s')

URL_PREFIX = '/api/v1/exness'
bp = Blueprint('transactions', __name__, url_prefix=URL_PREFIX)

# @bp.route('/transactions/accounts/<account>/statuses/<status>/payments/<payment_type>', methods=['GET'])
# @cross_origin()
# def exness_transaction_by_status_payment(account, status, payment_type):
#     logging.info(f"GET|{URL_PREFIX}/transactions/account/{account}/statuses/{status}/payments/{payment_type}:")
#     res = list_transaction_history(account=account, status=status, payment_type=payment_type)
#     return res, 200


@bp.route('/transactions', methods=['GET'])
@cross_origin()
def get_exness_transaction_history():
    account = request.args.get('account', type=str, default='') 
    payment = request.args.get('payment', type=str, default='') 
    status = request.args.get('status',   type=str, default='') 
    logging.info(f"GET|{URL_PREFIX}/transactions?account={account}&payment={payment}&status={status}")
    res = list_transaction_history(account=account, status=status, payment_type=payment)
    return res, 200


@bp.route('/transactions/latest', methods=['GET'])
@cross_origin()
def get_exness_transaction_history_latest(account, status):
    # check if account is available
    account = request.args.get('account', type=str, default='') 
    payment = request.args.get('payment', type=str, default='') 
    status = request.args.get('status',   type=str, default='') 
    logging.info(f"GET|{URL_PREFIX}/transactions/latest?account={account}&payment={payment}&status={status}")
    res = get_latest_transaction_history(account=account, status=status, payment_type=payment)
    return res, 200