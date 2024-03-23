from socket import socket
import json
import logging
import threading
from datetime import datetime
from ws_data_server import WebSocketServer


class OnTickPushServer:

    def __init__(self, port: int = 18765):
        self.ws_server = WebSocketServer(port=port)
    
    def publish(self, message):
        self.ws_server.publish(message)
    
    def start(self):
        threading.Thread(target=self.ws_server.start, daemon=True).start()


class Buffer:
    def __init__(self,sock):
        self.sock = sock
        self.buffer = b''

    def get_line(self):
        while b'\r\n' not in self.buffer:
            data = self.sock.recv(1024)
            if not data: # socket closed
                return None
            self.buffer += data
        line, sep, self.buffer = self.buffer.partition(b'\r\n')
        return line.decode()

class OnTickSocketServer:
    def __init__(self, socket_port: int = 19999, ws_port: int = 18765):
        self.s = socket()
        self.s.bind(('', socket_port))
        self.s.listen()
        logging.info(f'OnTickSocketServer {__class__}|Running: (press Ctrl+C to exit) 0.0.0.0:{socket_port}')
        self.ws = OnTickPushServer(port=ws_port)
        self.ws.start()

    def start(self):
        while True:
            conn, remote_addr = self.s.accept()
            with conn:
                logging.info(f'Connected:{remote_addr}')
                b = Buffer(conn)
                while True:
                    try:
                        line = b.get_line()
                        if line is None:
                            break
                        logging.info(f"RCV: {line}") 
                        tick = json.loads(line)
                        time = tick['time']
                        volume = tick['volume']
                        symbol = tick['symbol']
                        ask = tick['ask']
                        bid = tick['bid']
                        on_tick_event = {
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
                        "event" : "onTick",
                        "timestamp" : "2021-08-24 10:00:00",
                        "data" : {
                            time: "2021-08-24 10:00:00",
                            symbol: "BTCUSD"
                            ask: 1.1234,
                            bid: 1.1233,
                            volume: 1000
                        }
                        """
                        self.ws.publish(on_tick_event)
                    except Exception as e:
                        logging.exception(e)
                        break
            logging.info(f'Disconnected: {remote_addr}')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s|%(levelname)s|%(message)s')
    OnTickSocketServer(socket_port=29999, ws_port=18765).start()

