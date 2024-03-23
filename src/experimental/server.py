import time
import json
import logging

from flask import Flask, jsonify, request
from flask_sockets import Sockets
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
from werkzeug.routing import Rule

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s|%(name)s|%(levelname)s|%(message)s')

app = Flask(__name__)
sockets = Sockets(app)

@app.route('/api')
def my_restful_api():
    # 這裡放置RESTful API的代碼
    return jsonify(success=True, message="這是RESTful API的回應")


@sockets.route('/heartbeat', websocket=True)
def heartbeat(ws):
    lastres=""
    if request.environ.get("wsgi.websocket"):
        ws=request.environ["wsgi.websocket"]
        while 1:
            msg={"wsmsg":"message from flask websocket at %s"%(time.strftime("%Y-%m-%d,%H:%M:%S"))}
            ws.send(json.dumps(msg)) 
            time.sleep(10)
    return    


@sockets.route('/echo', websocket=True)
def echo(ws):
    while not ws.closed:
        message = ws.receive()
        if message:
            ws.send(message)


if __name__ == "__main__":
    # add echo route (https://github.com/heroku-python/flask-sockets/pull/82)
    sockets.url_map.add(Rule('/echo', endpoint=echo, websocket=True))
    sockets.url_map.add(Rule('/heartbeat', endpoint=heartbeat, websocket=True))

    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()
