import threading
import json
import logging

from flask import Flask, request

from __ws_data_server import WebSocketServer


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

    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
        self.ws_server = WebSocketServer()
        threading.Thread(target=self.ws_server.start).start()
        logging.info(f'WebSocket server started at {self.ws_server.host}:{self.ws_server.port}')


    def start(self):
        app = Flask(__name__)

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
            # notification = request.get_json()  # Get JSON data from the request

            # data = request.get_data(as_text=True) # Get raw data from the request
            # logging.info(f'RCV: {data}')
            # logging.info(f'RCV: {type(data)}')

            # URL of the management server
            # url = "http://{ip_address}/api"
            # response = requests.post(url, json=notification)
            # return f'Received the POST request and sent to management server: {response.json()}', response.status_code

            # parse data to json
            data = ''
            try: 
                data = request.get_data(as_text=True) # Get raw data from the request
                logging.debug(f'RCV(type): {type(data)}')
                logging.debug(f'RCV(data): [{data}]')

                json_data = json.loads(data)
                timestamp = json_data['timestamp']
                logging.debug(f'timestamp: {timestamp}')

                msg = json.dumps(json_data, indent=4)
                self.ws_server.publish(msg)
                logging.info(f'Published: {msg}')
                return f'Received the POST request and published it', 200
            except Exception as e:
                logging.error(f'error: [{e}], data: [{data}]', exc_info=True)
                return f'error: {e}', 400


        @app.route('/order', methods=['POST']) 
        def create_order():
            '''
            {
                "event": "order",
                "type": "3",
                "ticket": "123456789",
            }
            '''
            data = request.get_json()
            return 'Received the POST request', 200


        @app.route('/order', methods=['DELETE'])
        def delete_order():
            '''
            {
                "event": "order",
                "type": "3",
                "ticket": "123456789",
            }
            '''
            data = request.get_json()
            return 'Received the DELETE request', 200


        @app.route('/order', methods=['PUT'])
        def modify_order():
            '''
            {
                "event": "order",
                "type": "3",
                "ticket": "123456789",
            }
            '''
            data = request.get_json()
            return 'Received the DELETE request', 200


        @app.route('/position/list', methods=['GET'])
        def position_list():
            return 'Received the GET request', 200


        @app.route('/order/list', methods=['GET'])
        def order_list():
            return 'Received the GET request', 200  


        @app.route('/balance', methods=['GET'])
        def balance():
            return 'Received the GET request', 200


        @app.route('/ping', methods=['GET'])
        def ping():
            return 'pong', 200

        app.run(port=5000)




if __name__ == '__main__':
    MT5TradeServer().start()
    
