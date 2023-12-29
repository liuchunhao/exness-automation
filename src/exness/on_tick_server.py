from socket import socket
import json
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s|%(levelname)s|%(message)s|')

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

s = socket()
s.bind(('', 19999))
s.listen()
logging.info('Listening ... (press Ctrl+C to exit) @ 19999 ')
while True:
    c,a = s.accept()
    with c:
        logging.info('Connected:',a)
        b = Buffer(c)
        while True:
            try:
                line = b.get_line()
                if line is None:
                    break
                logging.info(f"recv: {line}") 
                order = json.loads(line)
                logging.info(f"{json.dumps(order, indent=4)}")
                # logging.info(f"order: {order['time']}, {order['ask']}, {order['bid']}, {order['volume']} ")
            except Exception as e:
                logging.error('Error:',e)
                break
    logging.info('Disconnected:',a)
