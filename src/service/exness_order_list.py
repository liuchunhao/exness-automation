#!/usr/bin/env python

import MetaTrader5 as mt5
import dotenv
import os
import logging

dotenv.load_dotenv()
# logging.basicConfig(filename='exness_order.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
logging.basicConfig(level=logging.INFO, format='%(asctime)s|%(levelname)s|%(message)s')

ACCOUNT = int(os.environ['ACCOUNT'])
SERVER = os.environ['SERVER']
PASSWORD = os.environ['PASSWORD']

logging.info(f'ACCOUNT: {ACCOUNT}, SERVER: {SERVER}, PASSWORD: {PASSWORD}') 

print("MetaTrader5 package author: ", mt5.__author__)
print("MetaTrader5 package version: ",mt5.__version__)

def init():
    # establish connection to the MetaTrader 5 terminal
    if not mt5.initialize(login=ACCOUNT, server=SERVER, password=PASSWORD):
        print("initialize() failed")
        print(mt5.last_error())
        mt5.shutdown()
        return False
    print('initialize() success')
    print(mt5.terminal_info())
    print(mt5.version())
    print(mt5.account_info())
    print(mt5.account_info()._asdict())
    return True


def send_order():
    res = mt5.order_send({
        'action': mt5.TRADE_ACTION_PENDING,
        'symbol': 'BTCUSD',
        'volume': 0.01,
        'type': mt5.ORDER_TYPE_BUY_LIMIT,
        'price': 7000,
        # 'sl': request['sl'],
        # 'tp': request['tp'],
        'deviation': 20,
        'magic': 234000,
        'comment': 'python limit order',
        'type_time': mt5.ORDER_TIME_GTC,
        'type_filling': mt5.ORDER_FILLING_RETURN,
    })
    print('order_send() done')


def limit_order(symbol='BTCUSDm', order_type, volume: float, price: float):
    type_dict = { 'buy': mt5.ORDER_TYPE_BUY_LIMIT, 'sell': mt5.ORDER_TYPE_SELL_LIMIT }  
    request = {
        'action': mt5.TRADE_ACTION_PENDING,  # Place an order for performing a deal at specified conditions (pending order)
        'symbol': symbol,
        'volume': volume,
        'type': type_dict[order_type],
        'price': price,
        'deviation': 20,
        'magic': 100,
        'comment': 'python limit order',
        'type_time': mt5.ORDER_TIME_GTC,
        'type_filling': mt5.ORDER_FILLING_RETURN,
    }
    result = mt5.order_send(request)
    if result is None:
        logging.warn(f'order_send() failed: {mt5.last_error()}')
        return None 
    logging.info(f'limit order sent: {result}')
    return result


def market_order(symbol='BTCUSDm', volume, order_type):
    tick = mt5.symbol_info_tick(symbol)
    logging.info(f'tick: {tick}')
    order_dict = { 'buy': mt5.ORDER_TYPE_BUY, 'sell': mt5.ORDER_TYPE_SELL }
    #price_dict = { 'buy': tick.ask, 'sell': tick.bid }
    request = {
        'action': mt5.TRADE_ACTION_DEAL,   # Place an order for an instant deal with the specified parameters (set a market order)
        'symbol': symbol,
        'volume': volume,
        'type': order_dict[order_type],
        # 'price': price_dict[order_type],
        # 'price': 1.0537,                    # 'price' is not used for market order, but required by 'order_send()
        'deviation': 20,
        'magic': 100,                       # what is this?  
        'comment': 'python market order',
        'type_time': mt5.ORDER_TIME_GTC,
        'type_filling': mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)
    if result is None:
        logging.warn(f'order_send() failed: {mt5.last_error()}')
        return None
    logging.info(f'buy market order sent: {result}')
    return result


def modify_order(symbol='BTCUSDm', volume, order_type):
    tick = mt5.symbol_info_tick(symbol)
    logging.info(f'tick: {tick}')
    order_dict = { 'buy': mt5.ORDER_TYPE_BUY, 'sell': mt5.ORDER_TYPE_SELL }
    #price_dict = { 'buy': tick.ask, 'sell': tick.bid }
    request = {
        'action': mt5.TRADE_ACTION_MODIFY,   # Change parameters of the previously placed trading order
        'symbol': symbol,
        'volume': volume,
        'type': order_dict[order_type],
        # 'price': price_dict[order_type],
        # 'price': 1.0537,                    # 'price' is not used for market order, but required by 'order_send()
        'deviation': 20,
        'magic': 100,                       # what is this?  
        'comment': 'python market order',
        'type_time': mt5.ORDER_TIME_GTC,
        'type_filling': mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)
    if result is None:
        logging.warn(f'order_send() failed: {mt5.last_error()}')
        return None
    logging.info(f'buy market order sent: {result}')
    return result


def delete_order(symbol='BTCUSDm', volume, order_type):
    tick = mt5.symbol_info_tick(symbol)
    logging.info(f'tick: {tick}')
    order_dict = { 'buy': mt5.ORDER_TYPE_BUY, 'sell': mt5.ORDER_TYPE_SELL }
    #price_dict = { 'buy': tick.ask, 'sell': tick.bid }
    request = {
        'action': mt5.TRADE_ACTION_REMOVE,      # Remove previously placed pending order
        'symbol': symbol,
        'volume': volume,
        'type': order_dict[order_type],
        # 'price': price_dict[order_type],
        # 'price': 1.0537,                      # 'price' is not used for market order, but required by 'order_send()
        'deviation': 20,
        'magic': 100,                           # what is this?  
        'comment': 'python market order',
        'type_time': mt5.ORDER_TIME_GTC,
        'type_filling': mt5.ORDER_FILLING_IOC,
    }
    result = mt5.order_send(request)
    if result is None:
        logging.warn(f'order_send() failed: {mt5.last_error()}')
        return None
    logging.info(f'buy market order sent: {result}')
    return result


def close_position(symbol='BTCUSDm', volume, order_type):
    tick = mt5.symbol_info_tick(symbol)
    logging.info(f'tick: {tick}')
    order_dict = { 'buy': mt5.ORDER_TYPE_BUY, 'sell': mt5.ORDER_TYPE_SELL }
    #price_dict = { 'buy': tick.ask, 'sell': tick.bid }
    request = {
        'action': mt5.TRADE_ACTION_CLOSE_BY,     # Close a position by an opposite one
        'symbol': symbol,
        'volume': volume,
        'type': order_dict[order_type],
        # 'price': price_dict[order_type],
        # 'price': 1.0537,                      # 'price' is not used for market order, but required by 'order_send()
        'deviation': 20,
        'magic': 100,                           # what is this?  
        'comment': 'python market order',
        'type_time': mt5.ORDER_TIME_GTC,
        'type_filling': mt5.ORDER_FILLING_IOC,
    }
    result = mt5.order_send(request)
    if result is None:
        logging.warn(f'order_send() failed: {mt5.last_error()}')
        return None
    logging.info(f'buy market order sent: {result}')
    return result


def get_symbol_info(symbol='BTCUSDm'):
    symbol_info = mt5.symbol_info(symbol)
    print('symbol_info:', symbol_info)
    return symbol_info


def get_all_symbols():
    # get all symbols
    symbols=mt5.symbols_get()
    print('Symbols: ', len(symbols))
    count=0
    # BTC
    for s in symbols:
        count+=1
        # if s.name has 'BTCUSD' in it
        if 'BTCUSD' in s.name:
            print("{}. {}".format(count,s.name))
            # print(s)
    print(mt5.last_error())
    print()




def get_all_orders():
    # check the presence of active orders
    orders = mt5.orders_total()
    if orders > 0:
        print("Total orders=", orders)
    else:
        print("Orders not found")
        print()


def get_order_by_ticket(ticket):
    order = mt5.orders_get(ticket=ticket)
    if order is None:
        logging.warn(f"No orders on {ticket}, error code={mt5.last_error()}") 
        return None
    logging.info(f'get_order_by_ticket: ticket={ticket}\n\r{order}')
    return order


def get_orders(symbol):
    orders = mt5.orders_get(symbol=symbol)
    if orders is None:
        logging.warn(f"No orders on {symbol}, error code={mt5.last_error()}") 
        return None
    for order in orders:
        logging.info(order)
        ticket = order.ticket   # 400019367
        order.time_setup        # 1710626732
        order.time_setup_msc    # 1710626732279
        order.time_done         # 0
        order.time_done_msc     # 0
        order.time_expiration   # 0
        order.type              # 2 
        order.type_time         # 0 
        order.type_filling      # 2 
        order.state             # 1 
        order.magic             # 100 
        order.position_id       # 0
        order.position_by_id    # 0
        order.reason            # 3
        order.volume_initial    # 0.01
        order.volume_current    # 0.01
        order.price_open        # 1.05
        order.sl                # 0.0
        order.tp                # 0.0
        order.price_current     # 65604.92
        order.price_stoplimit   # 0.0
        order.symbol            # 'BTCUSDm'
        order.comment           # 'python limit ord'
        order.external_id       # ''

        logging.info('ticket:', order.ticket, 'symbol:', order.symbol, 'volume:', order.volume_current, 'type:', order.type, 'price:', order.price)
        print()
        return orders


if __name__ == '__main__':
    init()
    # send_order()
    # limit_order('BTCUSDm', 0.01, 50000)
    print()
    # limit_order('EURUSDm', 'buy', volume=0.01, price=1.0537)
    # limit_order('BTCUSDm', 'buy', volume=0.01, price=65555)
    # market_order('EURUSD', 0.01, 'buy')  
    # get_symbol_info('BTCUSDm')
    # get_all_orders()

    # OK
    # get_all_symbols()
    # get_symbol_info('BTCUSDm')
    # get_orders('BTCUSDm')
    get_order_by_ticket(ticket=400019367)

    mt5.shutdown()
