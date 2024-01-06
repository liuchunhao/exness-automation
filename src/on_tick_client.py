import json
import logging
import threading
import time

import rel
import websocket
from websocket._app import WebSocketApp

import os
from dotenv import load_dotenv


logger = logging.getLogger(__name__)

# 建立一個事件物件
stop_event = threading.Event()

def on_message(ws, message):
    data = json.loads(message)
    logging.info(f'on_message: {json.dumps(data, indent=4)}')

def on_error(ws, error):
    logging.error(f'error: {error}')

def on_close(ws, close_status_code, close_msg):
    logging.info(f"on_close: {ws.url}, status_code:{close_status_code}, msg:{close_msg}")

def on_open(ws):
    logging.info(f"on_open: {ws.url}")

from abc import ABC, abstractmethod
class Handler(ABC):
    @abstractmethod
    def on_tick_exness(self, tick: dict):
        """
        {
            "event" : "onTick",
            "from" : "exness",
            "timestamp" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "data" : {
                "time": time,
                "symbol": symbol,
                "ask": ask,
                "bid": bid,
                "volume": volume
            }
        }
        """

    @abstractmethod
    def on_tick_binance(self, tick: dict):
        """
        {
            "event" : "onTick",
            "from" : "binance",
            "timestamp" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "data" : {
                "time": time,
                "symbol": symbol,
                "ask": ask,
                "bid": bid,
                "volume": volume
            }
        }
        """
        pass

    @abstractmethod
    def on_trade_exness(self, trade: dict):
        """
        {
            "event": "TRADE_TRANSACTION_HISTORY_ADD",
            "timestamp": "2024.01.06 05:58:49",
            "account": {
                "timestamp": "2024.01.06 05:58:49",
                "accountLogin": 41084529,
                "balance": 99982.21,
                "profit": 11.77,
                "margin": 2.22,
                "freeMargin": 99991.76,
                "marginLevel": 4504233.33
            },
            "orders": {
                "timestamp": "2024.01.06 05:58:49",
                "data": []
            },
            "positions": {
                "timestamp": "2024.01.06 05:58:49",
                "data": [
                    {
                        "ticket": 36766067,
                        "symbol": "BTCUSD",
                        "volume": 45000.00,
                        "priceOpen": 12.81,
                        "profit": 0.00
                    },
                    {
                        "ticket": 36793203,
                        "symbol": "BTCUSD",
                        "volume": 43615.18,
                        "priceOpen": -1.04,
                        "profit": 0.00
                    }
                ]
            }
        }
        """


class WebSocketClient:

    def __init__(self, handler: Handler) -> None:
        self.handler = handler
        websocket.enableTrace(False)
        load_dotenv()

    def rcv_event_exness(self):
        url = os.getenv("URL_EXNESS_WS_EVENT") or "ws://localhost:8765"
        if url is None:
            raise ValueError("URL_EXNESS_WS_EVENT is not set") 
        ws = WebSocketApp(url,
                                on_open=on_open,
                                on_message=lambda ws, msg: self.handler.on_trade_exness(json.loads(msg)),
                                on_error=on_error,
                                on_close=on_close)
        # ws.run_forever(dispatcher=rel, reconnect=5)  
        # rel.signal(2, rel.abort)    
        # rel.dispatch()              
        while not stop_event.is_set():
            try:
                ws.run_forever(ping_interval=60, ping_timeout=30)
            except Exception as e:
                logging.error(f'ws.run_forever: {e}')
                time.sleep(1)



    
    def rcv_tick_exness(self):
        url = os.getenv("URL_EXNESS_WS_TICK") or "ws://localhost:18765"
        if url is None:
            raise ValueError("URL_EXNESS_WS_TICK is not set")
        ws = WebSocketApp(url,
                            on_open=on_open,
                            on_message=lambda ws, msg: self.handler.on_tick_exness(json.loads(msg)),
                            on_error=on_error,
                            on_close=on_close)
        ws.run_forever(dispatcher=rel, reconnect=5)  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
        rel.signal(2, rel.abort)                     # Keyboard Interrupt
        rel.dispatch()                               # Start the event loop

        # while not stop_event.is_set():
        #     try:
        #         ws.run_forever(ping_interval=60, ping_timeout=30)
        #     except Exception as e:
        #         logging.error(f'ws.run_forever: {e}')
        #         time.sleep(1)




    def rcv_tick_binance(self):
        url = os.getenv("URL_BN_WS_TICK") or "ws://localhost:28765"
        ws = WebSocketApp(url,
                                on_open=on_open,
                                on_message=lambda ws, msg: self.handler.on_tick_binance(json.loads(msg)),
                                on_error=on_error,
                                on_close=on_close)
        # ws.run_forever(dispatcher=rel, reconnect=5)  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
        # rel.signal(2, rel.abort)                     # Keyboard Interrupt
        # rel.dispatch()                               # Start the event loop

        # while not stop_event.is_set():
        #     logging.info(f'stop_event|rcv_tick_binance: {url}')
        #     ws.run_forever()
        
        while not stop_event.is_set():
            try:
                ws.run_forever(ping_interval=60, ping_timeout=30)
            except Exception as e:
                logging.error(f'ws.run_forever: {e}')
                time.sleep(1)



    def on_event_binance(self):
        pass
        # TODO: implement on_bn_event


    def start(self):
        # self.rcv_event_exness()
        self.rcv_tick_exness()

        # threading.Thread(target=self.rcv_event_exness, daemon=True).start()
        # threading.Thread(target=self.rcv_tick_exness, daemon=True).start()
        # threading.Thread(target=self.rcv_tick_binance, daemon=True).start()
        # while True:
        #     # run forever
        #     time.sleep(1)
        


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s|%(levelname)s|%(message)s')

    class MyHandler(Handler):
        def on_tick_exness(self, data):
            # Implement the logic for handling tick data from Exness
            logging.info(f'on_tick_exness: {data}')

        def on_tick_binance(self, data):
            # Implement the logic for handling tick data from Binance
            logging.info(f'on_tick_binance: {data}')

        def on_trade_exness(self, data):
            # Implement the logic for handling trade data from Exness
            logging.info(f'on_trade_exness: {data}')    

        def on_event_binance(self, data):
            # Implement the logic for handling event data from Binance
            logging.info(f'on_event_binance: {data}')

    handler = MyHandler()
    WebSocketClient(handler=handler).start()
