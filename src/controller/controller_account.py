from flask import Blueprint, request
from flask_cors import cross_origin

from service.exness_order import get_account_info

URL_PREFIX = '/api/v1/exness'
bp = Blueprint('account', __name__, url_prefix=URL_PREFIX)


@bp.route('/account_info', methods=['GET'])
@cross_origin()
def exness_account_info():
    res = get_account_info()
    if res is None:
        return 'No account info found', 404
    return res, 200


@bp.route('/balance', methods=['GET'])
@cross_origin()
def exness_balance_info():
    res = get_account_info()
    if res is None:
        return 'No account info found', 404
    login = res['login']
    balance = float(res['balance'])
    profit = float(res['profit'])
    equity = float(res['equity'])
    return {
        "login": login,
        "balance": balance,
        "profit": profit,
        "equity": equity
    }, 200


@bp.route('/margin', methods=['GET'])
@cross_origin()
def exness_margin():
    res = get_account_info()
    if res is None:
        return 'No account info found', 404
    login = res['login']
    equity = float(res['equity'])
    margin = float(res['margin'])
    margin_free = float(res['margin_free'])
    return {
        "login": login,
        "margin": margin,
        "margin_free": margin_free,
        "equity": equity
    }, 200


@bp.route('/equity', methods=['GET'])
@cross_origin()
def exness_equity():
    res = get_account_info()
    if res is None:
        return 'No account info found', 404
    login = res['login']
    equity = float(res['equity'])
    return {
        "login": login,
        "equity": equity
    }, 200
