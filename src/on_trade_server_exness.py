import threading
import json
import logging

from flask import Flask, request
from flask_cors import CORS

from ws_data_server import WebSocketServer


class MT5TradeServer:
    '''
    a server to interact with MT5 for the following :
    1. onTrade event notification and send to management server
    2. create order
    3. delete order
    4. modify order
    5. position list
    6. order list
    '''

    def __init__(self, api_port=5000, ws_port=8765):
        self.api_port = api_port
        self.ws_server = WebSocketServer(port=ws_port)
        threading.Thread(target=self.ws_server.start, daemon=True).start()
        logging.info(f'WebSocket server started at {self.ws_server.host}:{self.ws_server.port}')


    def start(self):
        app = Flask(__name__)
        CORS(app)

        @app.errorhandler(Exception)
        def server_error(err):
            app.logger.exception(err)
            return {
                "code": -1,
                "msg": f"{err}",
                "data": []
            }, 200
        
        
        @app.route('/sms', methods=['POST'])
        def sms():
            '''
            {
                timestamp: '2021-09-08 12:34:56'
                from: '+886958123456',
                msg: 'hello world'
            }
            '''
            data = ''
            try: 
                data = request.get_data(as_text=True) 
                logging.debug(f'RCV: [{data}]')
                # json_data = json.loads(data)
                # timestamp = json_data['timestamp']
                self.ws_server.publish(data)
                logging.info(f'SND: {data}')
                return f'Received the POST request and published it', 200
            except Exception as e:
                logging.error(f'error: [{e}], data: [{data}]', exc_info=True)
                return f'error: {e}', 400


        @app.route('/notification/trade', methods=['POST'])
        def on_trade():
            '''
            To receive MT5 onTrade event notification and send to management server
            {
                "event": "onTrade",
                "type": "3",
                "ticket": "123456789",
            }
            '''
            data = ''
            try: 
                data = request.get_data(as_text=True) # Get raw data from the request
                logging.info(f'RCV: [{type(data)}]|{data}')
                self.ws_server.publish(data)
                logging.info(f'SND: {data}')
                return f'Received the POST request and published it', 200
            except Exception as e:
                logging.error(f'error: [{e}], data: [{data}]', exc_info=True)
                return f'error: {e}', 400


        from controller import controller_order, controller_heartbeat, controller_account 
        
        app.register_blueprint(controller_order.bp)
        app.register_blueprint(controller_heartbeat.bp)
        app.register_blueprint(controller_account.bp)

        app.run(port=self.api_port, debug=False)


        def shutdown_server():
            func = request.environ.get('werkzeug.server.shutdown')
            if func is None:
                raise RuntimeError('Not running with the Werkzeug Server')
            func()



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s|%(levelname)s|%(message)s')
    MT5TradeServer(api_port=5000, ws_port=8765).start()
    
