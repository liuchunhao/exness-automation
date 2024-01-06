import websocket
import json
import logging
import datetime
import rel
import threading

logger = logging.getLogger(__name__)
    
# 訂閱深度資訊
def on_open(ws):
    symbol = 'btcusdt'
    level = 5
    msg = {
        "method": "SUBSCRIBE",
        "params":
        [
          # "btcusd_perp@ticker",
          # "btcusd@ticker",
          f"{symbol}@depth{level}",
        ],
        "id": 1
    }
    res = ws.send(json.dumps(msg))
    logging.info(f'on_open:{res}')

def on_error(ws, error):
    logging.error(f'error: {error}')
    
def on_close(ws, close_status_code, close_msg):
    logging.info("### closed ###")



"""

# ws = websocket.WebSocketApp("wss://fstream.binance.com/ws",
#                            on_open=on_open,
#                            on_message=on_message)

# ws = websocket.WebSocketApp("wss://fstream.binance.com/stream?streams=btcusdt@ticker",   on_message=on_message)    
# ws = websocket.WebSocketApp("wss://fstream.binance.com/stream?streams=btcusdt@aggTrade", on_message=on_message)  

"""

from ws_data_server import WebSocketServer

class BinanceOnTickServer:

    def __init__(self, port) -> None:
        self.ws_server = WebSocketServer(port=port)
        threading.Thread(target=self.ws_server.start, daemon=True).start()

        def on_message(ws, message):
            msg = json.loads(message)
            # logging.info(f'on_message: {json.dumps(msg, indent=4)}')

            data = msg['data']
            # unix time to datetime
            timestamp = datetime.datetime.fromtimestamp(int(data['E'])/1000)

            bids = data['b']
            bid = bids[0]
            b_px = bid[0]
            b_qty = bid[1]

            asks = data['a']
            ask = asks[0]
            a_px = ask[0]
            a_qty = ask[1]

            # output = f'on_message: {timestamp};  bid:[px:{b_px} qty:{b_qty}]  ask:[px:{a_px} qty:{a_qty}]'
            output = {
                "event" : "onTick",
                "from" : "binance",
                "timestamp" : timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "data" : {
                    "time": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    "symbol": "BTCUSD",
                    "ask": a_px,
                    "bid": b_px,
                    "ask_qty": a_qty,
                    "bid_qty": b_qty
                }
            }
            logging.info(f'RCV: {output}')
            self.ws_server.publish(output)
            

        symbol = 'btcusdt'
        levels = 5      # 5, 10, 20
        speed = '100'   # 500ms, 250ms, 100ms 
        self.ws = websocket.WebSocketApp(f"wss://fstream.binance.com/stream?streams={symbol}@depth{levels}@{speed}ms",
        # ws = websocket.WebSocketApp(f"wss://fstream.binance.com/stream?streams=btcusdt@depth5",
                                    # on_open=on_open, 
                                    # on_data=on_data, 
                                    # on_cont_message=on_cont_message, 
                                    # on_cont_error=on_cont_error, 
                                    # on_cont_close=on_cont_close, 
                                    # on_cont_data=on_cont_data,
                                    on_error=on_error, 
                                    on_close=on_close, 
                                    on_message=on_message)

        logging.info(f'ws: {self.ws}')


    def start(self):
        self.ws.run_forever(dispatcher=rel, reconnect=5)     # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
        rel.signal(2, rel.abort)                             # Keyboard Interrupt
        rel.dispatch()                                       # Start the event loop


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s|%(levelname)s|%(message)s')
    BinanceOnTickServer(port=28765).start()


