import rel
import websocket
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s|%(levelname)s|%(message)s')
logger = logging.getLogger(__name__)

def on_message(ws, message):
    msg = json.loads(message)
    logger.info(json.dumps(msg, indent=4))

def on_error(ws, error):
    logging.error(error)

def on_close(ws, close_status_code, close_msg):
    logging.info("### closed ###")

def on_open(ws):
    logging.info("Opened connection")

if __name__ == "__main__":
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp("wss://api.gemini.com/v1/marketdata/BTCUSD",
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever(dispatcher=rel, reconnect=5)  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
    rel.signal(2, rel.abort)    # Keyboard Interrupt
    rel.dispatch()              # Start the event loop