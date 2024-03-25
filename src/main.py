import datetime
import logging

from flask import Flask, request, abort, g
from flask_cors import CORS

# from flask_sockets import Sockets
# from flask import jsonify

# import gevent
# from gevent.pywsgi import WSGIServer
# from geventwebsocket.handler import WebSocketHandler

from controller import controller_heartbeat
from controller import controller_withdraw
from controller import controller_order
from controller import controller_account
from controller import controller_position
from controller import controller_transaction_history

from service.exness_order import init

logging.basicConfig(level=logging.INFO, format='%(asctime)s|%(name)s|%(levelname)s|%(message)s')

app = Flask(__name__)
CORS(app)
# sockets = Sockets(app)

app.register_blueprint(controller_heartbeat.bp)
app.register_blueprint(controller_withdraw.bp)
app.register_blueprint(controller_order.bp)
app.register_blueprint(controller_account.bp)
app.register_blueprint(controller_position.bp)
app.register_blueprint(controller_transaction_history.bp)

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

    # import threading
    # from on_tick_server_exness import OnTickSocketServer
    # from on_trade_server_exness import MT5TradeServer

    # def run_on_tick_server():
    #     on_tick_server = OnTickSocketServer(socket_port=29999, ws_port=18765)
    #     on_tick_server.start()

    # def run_on_trade_server():
    #     on_trade_server = MT5TradeServer(api_port=5000, ws_port=8765)
    #     on_trade_server.start()

    # threading.Thread(target=run_on_trade_server).start()
    # threading.Thread(target=run_on_tick_server).start()

    app.run(port=5100, debug=True)
