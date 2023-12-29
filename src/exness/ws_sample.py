import websocket
import json
import logging
import datetime

logging.basicConfig(level=logging.DEBUG)

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
    

def on_message(ws, message):
    msg = json.loads(message)
    data = msg['data']

    # transform unix time to datetime
    timestamp = datetime.datetime.fromtimestamp(int(data['E'])/1000)

    bids = data['b']
    bid = bids[0]
    b_px = bid[0]
    b_qty = bid[1]

    asks = data['a']
    ask = asks[0]
    a_px = ask[0]
    a_qty = ask[1]
    logging.info(f'on_message: update: {timestamp};  bid:[px:{b_px} qty:{b_qty}]  ask:[px:{a_px} qty:{a_qty}]')

# ws = websocket.WebSocketApp("wss://fstream.binance.com/ws",
#                            on_open=on_open,
#                            on_message=on_message)

# ws = websocket.WebSocketApp("wss://fstream.binance.com/stream?streams=btcusdt@ticker", on_message=on_message)    
# ws = websocket.WebSocketApp("wss://fstream.binance.com/stream?streams=btcusdt@aggTrade", on_message=on_message)  

symbol = 'btcusdt'
levels = 5      # 5, 10, 20
speed = '100'   # 500ms, 250ms, 100ms 
ws = websocket.WebSocketApp(f"wss://fstream.binance.com/stream?streams={symbol}@depth{levels}@{speed}ms",
# ws = websocket.WebSocketApp(f"wss://fstream.binance.com/stream?streams=btcusdt@depth5",
                            # on_open=on_open, 
                            on_error=on_error, 
                            # on_close=on_close, 
                            # on_data=on_data, 
                            # on_cont_message=on_cont_message, 
                            # on_cont_error=on_cont_error, 
                            # on_cont_close=on_cont_close, 
                            # on_cont_data=on_cont_data,
                            on_message=on_message)


if __name__ == '__main__':
    # 開始執行
    ws.run_forever()


