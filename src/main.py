import datetime
import logging

from flask import Flask, request, abort, g
from flask_cors import CORS

from controller import controller_heartbeat
from controller import controller_withdraw
from controller import controller_order
from controller import controller_account
from controller import controller_position
from controller import controller_transaction_history
from controller import controller_wallet

from service.exness_order import init

logging.basicConfig(level=logging.INFO, format='%(asctime)s|%(name)s|%(levelname)s|%(message)s')

app = Flask(__name__)
CORS(app)

app.register_blueprint(controller_heartbeat.bp)
app.register_blueprint(controller_withdraw.bp)
app.register_blueprint(controller_order.bp)
app.register_blueprint(controller_account.bp)
app.register_blueprint(controller_position.bp)
app.register_blueprint(controller_transaction_history.bp)
app.register_blueprint(controller_wallet.bp)

clients = set()


@app.errorhandler(Exception)
def server_error(err):
    app.logger.exception(err)
    return {
        "code": -1,
        "msg": f"{err}",
        "data": []
    }, 200


# @app.after_request  # after each request
# def after_request(response):
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
#     response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')


if __name__ == '__main__':
    init()
    app.run(host='0.0.0.0', port=5300, debug=True)
