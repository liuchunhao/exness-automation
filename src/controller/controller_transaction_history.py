from flask import Blueprint, request
from flask_cors import cross_origin

from service.exness_transaction_history import get_withdrawal_status
from service.exness_transaction_history import list_withdrawal_history

import logging
import json
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s|%(name)s|%(levelname)s|%(message)s')

URL_PREFIX = '/api/v1/exness'
bp = Blueprint('transactions', __name__, url_prefix=URL_PREFIX)

@bp.route('/transactions/accounts/<account>', methods=['GET'])
@cross_origin()
def exness_transaction(account):
    logging.info(f"GET|{URL_PREFIX}/transactions/accounts/{account}:")
    res = get_withdrawal_status(account=account)
    # TODO: 
    # exness_withdraw(network=data['network'], address=data['address'], amount=data['amount'])
    # [X] get_withdrawal_status(account=account, invoice_id=invoice_id)
    # [X] get_withdrawal_status(account=account)
    # [X] list_withdrawal_history(account=account, status="Rejected", payment_type="transfer")
    # [X] list_withdrawal_history(account=account, status="Rejected", payment_type="withdrawal")
    # [X] list_withdrawal_history(account=account, status="Rejected", payment_type="deposit")
    # [X] list_withdrawal_history(account=account, status="Done", payment_type="deposit")
    return res, 200


@bp.route('/transactions/accounts/<account>/invoices/<invoice_id>', methods=['GET'])
@cross_origin()
def exness_transaction_by_invoice(account, invoice_id):
    logging.info(f"GET|{URL_PREFIX}//transactions/account/{account}/invoices/{invoice_id}:")
    res = get_withdrawal_status(account=account, invoice_id=invoice_id)
    # TODO: 
    # exness_withdraw(network=data['network'], address=data['address'], amount=data['amount'])
    # [X] get_withdrawal_status(account=account, invoice_id=invoice_id)
    # [X] get_withdrawal_status(account=account)
    # [X] list_withdrawal_history(account=account, status="Rejected", payment_type="transfer")
    # [X] list_withdrawal_history(account=account, status="Rejected", payment_type="withdrawal")
    # [X] list_withdrawal_history(account=account, status="Rejected", payment_type="deposit")
    # [X] list_withdrawal_history(account=account, status="Done", payment_type="deposit")
    return res, 200


@bp.route('/transactions/accounts/<account>/statuses/<status>/payments/<payment_type>', methods=['GET'])
@cross_origin()
def exness_transaction_by_status_payment(account, status, payment_type):
    logging.info(f"GET|{URL_PREFIX}/transactions/account/{account}/statuses/{status}/payments/{payment_type}:")
    res = list_withdrawal_history(account=account, status=status, payment_type=payment_type)
    return res, 200