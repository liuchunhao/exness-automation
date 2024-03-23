#!/usr/bin/env python

import os
import logging
import datetime
import dotenv

import MetaTrader5 as mt5

from service.exness_error import get_error_message

logging.basicConfig(level=logging.INFO, format='%(asctime)s|%(levelname)7s|%(message)s')

dotenv.load_dotenv()

ACCOUNT = int(os.environ['ACCOUNT'])
SERVER = os.environ['SERVER']
PASSWORD = os.environ['PASSWORD']

logging.info(f'ACCOUNT: {ACCOUNT}, SERVER: {SERVER}, PASSWORD: {PASSWORD}') 
logging.info(f"MetaTrader5 package author:  {mt5.__author__}")
logging.info(f"MetaTrader5 package version: {mt5.__version__}")


def utc_from_timestamp(timestamp: int):
    return datetime.datetime.utcfromtimestamp(timestamp/1000).strftime('%Y-%m-%d %H:%M:%S')


def init():
    # establish connection to the MetaTrader 5 terminal
    if not mt5.initialize(login=ACCOUNT, server=SERVER, password=PASSWORD):
        logging.info(f"initialize() failed: {mt5.last_error()}")
        mt5.shutdown()
        return False

    logging.info(f'initialize() success, terminal_info: {mt5.terminal_info()}')
    return True


def get_account_info():
    '''
    AccountInfo(login=41084529, trade_mode=0, leverage=500, limit_orders=1024, margin_so_mode=0, trade_allowed=True, trade_expert=True, margin_mode=2, currency_digits=2, fifo_close=False, balance=99605.16, credit=0.0, profit=-21.36, equity=99583.8, margin=14.75, margin_free=99569.05, margin_level=675144.4067796611, margin_so_call=30.0, margin_so_so=0.0, margin_initial=0.0, margin_maintenance=0.0, assets=0.0, liabilities=0.0, commission_blocked=0.0, name='裸点账户', server='Exness-MT5Trial3', currency='USD', company='Exness Technologies Ltd'), (1, 'Success')
    '''
    account_info = mt5.account_info()
    logging.info(f'account_info: {account_info}, {mt5.last_error()}')

    account_info = account_info._asdict()
    logging.info(f'account_info: {account_info}, {mt5.last_error()}')
    logging.info(f'balance: {account_info["balance"]}')
    logging.info(f'profit: {account_info["profit"]}')
    logging.info(f'equity: {account_info["equity"]}')
    logging.info(f'margin: {account_info["margin"]}')
    logging.info(f'margin_free: {account_info["margin_free"]}')
    logging.info(f'margin_level: {account_info["margin_level"]}%')
    logging.info(f'currency: {account_info["currency"]}')
    logging.info(f'login: {account_info["login"]}')
    return account_info


def limit_order(symbol: str, order_type: str, volume: float, price: float, type_filling=mt5.ORDER_FILLING_RETURN):
    type_dict = { 'buy': mt5.ORDER_TYPE_BUY_LIMIT, 'sell': mt5.ORDER_TYPE_SELL_LIMIT }  
    request = {
        'action': mt5.TRADE_ACTION_PENDING,  # Place an order for performing a deal at specified conditions (pending order)
        'symbol': symbol,                    # 'BTCUSD'
        'volume': float(volume),
        'type': type_dict[order_type],
        'price': float(price),
        'comment': 'limit order',
        'type_time': mt5.ORDER_TIME_GTC,
        'type_filling': type_filling,        # https://www.mql5.com/en/docs/constants/tradingconstants/orderproperties#enum_order_type_filling
    }
    result = mt5.order_send(request)
    if result is None:
        logging.warning(f'limit_order failed: {mt5.last_error()}')
        return None 

    if result.retcode != mt5.TRADE_RETCODE_DONE:
        err_msg = get_error_message(result.retcode)
        logging.info(f"limit_order failed, retcode={result.retcode}, {err_msg}")

    logging.info(f'limit_order sent: {result}, {mt5.last_error()}')
    return result._asdict()


def market_order(symbol, volume: float, order_type: str):
    tick = mt5.symbol_info_tick(symbol)
    logging.info(f'tick: {tick}')
    price_dict = { 'buy': tick.ask, 'sell': tick.bid }
    order_dict = { 'buy': mt5.ORDER_TYPE_BUY, 'sell': mt5.ORDER_TYPE_SELL }
    request = {
        'action': mt5.TRADE_ACTION_DEAL,    # Place an order for an instant deal with the specified parameters (set a market order)
        'symbol': symbol,                   # 'BTCUSD'
        'volume': volume,
        'type': order_dict[order_type],
        'price': price_dict[order_type],    # 'price' is not used for market order, but required by 'order_send()
        'deviation': 20,
        'magic': 100,                       # EA ID
        'comment': 'market order',
        'type_time': mt5.ORDER_TIME_GTC,
        'type_filling': mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)
    if result is None:
        logging.warning(f'market_order failed: {mt5.last_error()}')
        return None

    if result.retcode != mt5.TRADE_RETCODE_DONE:
        logging.info(f"market_order failed, retcode={result.retcode}")

    logging.info(f'market_order sent: {result}, {mt5.last_error()}')
    return result._asdict()


def modify_order_by_price(ticket: int, price: float):
    # order_dict = { 'buy': mt5.ORDER_TYPE_BUY, 'sell': mt5.ORDER_TYPE_SELL }
    request = {
        'action': mt5.TRADE_ACTION_MODIFY,      # Change parameters of the previously placed trading order
        'order': ticket,                        # 'order' is the ticket of the order to be modified
        'price': float(price),              # 'price' is not used for market order, but required by 'order_send()
        # 'volume': float(volume),
        'deviation': 20,
        'magic': 100,                       
        'comment': 'modify_order',
        # 'type_time': mt5.ORDER_TIME_GTC,
        # 'type_filling': mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)
    if result is None:
        logging.warning(f'modify_order failed: {mt5.last_error()}')
        return None

    if result.retcode != mt5.TRADE_RETCODE_DONE:
        logging.info(f"modify_order failed, retcode={result.retcode}")

    logging.info(f'modify_order sent: {result}, {mt5.last_error()}')
    return result._asdict()


def delete_order(ticket: int):
    request = {
        'action': mt5.TRADE_ACTION_REMOVE,      # Remove previously placed pending order
        'order': ticket,
        'comment': 'delete_order',
    }
    result = mt5.order_send(request)
    if result is None:
        logging.warning(f'delete_order (ticket={ticket}) failed: {mt5.last_error()}')
        return None
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        logging.info(f"delete_order (ticket={ticket}) failed, retcode={result.retcode}")

    logging.info(f'delete_order (ticket={ticket}) sent: {result}, {mt5.last_error()}')
    return result._asdict()


def get_position(ticket):
    '''
        get position on ticket
        ticket=47106357, time=1710736375, time_msc=1710736375360, time_update=1710736375, time_update_msc=1710736375360, type=0, magic=100, identifier=47106357, reason=3, volume=0.02, price_open=68037.02, sl=0.0, tp=0.0, price_current=66892.11, swap=0.0, profit=-22.9, symbol='BTCUSD', comment='market order', external_id=''
    '''
    position = mt5.positions_get(ticket=ticket)[0]
    if position is None:
        logging.warning(f"get_position: No position on ticket = {ticket}, error code={mt5.last_error()}") 
        return None
    logging.info(f'get_position on ticket = {ticket}: {position}, {mt5.last_error()}')
    position_dict = position._asdict()
    time_update_msc = utc_from_timestamp(position.time_update_msc)
    time_msc = utc_from_timestamp(position.time_msc)
    position_dict['time_update_msc'] = time_update_msc
    position_dict['time_msc'] = time_msc
    position_dict['type'] = 'buy' if position_dict['type'] == mt5.ORDER_TYPE_BUY else 'sell'
    logging.info(f'get_position on ticket = {ticket}: {position_dict}, {mt5.last_error()}')
    return position_dict


def get_all_positions(symbol='BTCUSD'):
    # get all positions on BTCUSD
    positions = mt5.positions_get(symbol='BTCUSD')
    if positions is None:
        logging.warning(f"get_all_positions: No positions on {symbol}, error code={mt5.last_error()}") 
        return None
    logging.info(f'get_all_positions: {positions}, {mt5.last_error()}')
    n = 0
    count = len(positions)
    position_dict = {}
    position_dict['count'] = count
    position_dict['symbol'] = symbol
    position_dict['positions'] = [position._asdict() for position in positions]

    for position in position_dict['positions']:
        '''
        ticket=47106357, time=1710736375, time_msc=1710736375360, time_update=1710736375, time_update_msc=1710736375360, type=0, magic=100, identifier=47106357, reason=3, volume=0.02, price_open=68037.02, sl=0.0, tp=0.0, price_current=66892.11, swap=0.0, profit=-22.9, symbol='BTCUSD', comment='market order', external_id=''
        '''

        n += 1
        time_update_msc = utc_from_timestamp(position['time_update_msc'])
        time_msc = utc_from_timestamp(position['time_msc'])
        position['time_update_msc'] = time_update_msc
        position['time_msc'] = time_msc
        position['type'] = 'buy' if position['type'] == mt5.ORDER_TYPE_BUY else 'sell'
        logging.info(f'get_all_positions[{n}/{count}]: {position}')

    return position_dict



def close_position(ticket: int):
    positions= mt5.positions_get(ticket=ticket)
    position = positions[0] if len(positions) > 0 else None
    if position is None:
        logging.warning(f"close_position: No position on {ticket}, error code={mt5.last_error()}") 
        return None
    tick = mt5.symbol_info_tick(position.symbol)
    request = {
        'action': mt5.TRADE_ACTION_DEAL,        # Place an order for an instant deal with the specified parameters (set a market order)
        'symbol': position.symbol,              # 'BTCUSD'
        'position': ticket,                         
        'volume': position.volume,
        'type': mt5.ORDER_TYPE_SELL if position.type == mt5.ORDER_TYPE_BUY else mt5.BOOK_TYPE_BUY,
        'price': tick.bid if position.type == mt5.ORDER_TYPE_BUY else tick.ask,
        'comment': 'close_position',           # less than 14 characters
    }
    result = mt5.order_send(request)
    if result is None:
        logging.warning(f'close_position failed on ticket = {ticket} : {mt5.last_error()}')
        return None
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        logging.info(f"close_position failed on ticket = {ticket} , retcode={result.retcode}")

    logging.info(f'close_position on ticket = {ticket} sent: {result}, {mt5.last_error()}')
    res = result._asdict()
    return res


def close_position_by_volume(ticket: int, volume: float):
    '''
        OrderSendResult(retcode=10009, deal=34621560, order=47680492, volume=0.01, price=67889.22, bid=67889.22, ask=67913.54000000001, comment='close position', request_id=3922353990, retcode_external=0, request=TradeRequest(action=1, magic=0, order=0, symbol='BTCUSD', volume=0.01, price=67889.22, stoplimit=0.0, sl=0.0, tp=0.0, deviation=0, type=1, type_filling=0, type_time=0, expiration=0, comment='close position', position=47247020, position_by=0))
    '''
    positions= mt5.positions_get(ticket=ticket)
    position = positions[0] if len(positions) > 0 else None
    if position is None:
        logging.warning(f"close_position: No position on {ticket}, error code={mt5.last_error()}") 
        return None

    tick = mt5.symbol_info_tick(position.symbol)
    request = {
        'action': mt5.TRADE_ACTION_DEAL,        # Place an order for an instant deal with the specified parameters (set a market order)
        'symbol': position.symbol,              # 'BTCUSD'
        'position': ticket,                         
        'volume': volume,
        'type': mt5.ORDER_TYPE_SELL if position.type == mt5.ORDER_TYPE_BUY else mt5.BOOK_TYPE_BUY,
        'price': tick.bid if position.type == mt5.ORDER_TYPE_BUY else tick.ask,
        'comment': "close_position_by_volume",
    }
    result = mt5.order_send(request)
    if result is None:
        logging.warning(f'close_position failed on ticket = {ticket} by volume = {volume}: {mt5.last_error()}')
        return None
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        logging.info(f"close_position failed on ticket = {ticket} by volume = {volume}, retcode={result.retcode}")
    logging.info(f'close_position on ticket = {ticket} by volume = {volume} sent: {result}, {mt5.last_error()}')
    res = result._asdict()
    return res


def get_symbol_info(symbol='BTCUSD'):
    symbol_info = mt5.symbol_info(symbol)
    logging.info(f'get_symbol_info: {symbol_info}')
    logging.info(f'get_symbol_info: {mt5.last_error()}')
    return symbol_info


def get_all_symbols():
    # get all symbols
    symbols=mt5.symbols_get()
    logging.info(f'get_all_symbols: {len(symbols)} symbols')
    count=0
    for s in symbols:
        count+=1
        # if 'BTCUSD' in s.name:
        logging.info("{}. {}".format(count, s.name))
    logging.info(f'get_all_symbols: {mt5.last_error()}')
    return symbols


def get_order_by_ticket(ticket: int):
    order = mt5.orders_get(ticket=ticket)
    if order is None:
        logging.warning(f"get_order_by_ticket: No orders on {ticket}, error code={mt5.last_error()}")
        return None

    if len(order) == 0:
        logging.warning(f"get_order_by_ticket: No orders on {ticket}, error code={mt5.last_error()}") 
        return None

    '''
    TradeOrder(ticket=47247319, time_setup=1710822767, time_setup_msc=1710822767092, time_done=0, time_done_msc=0, time_expiration=0, type=2, type_time=0, type_filling=2, state=1, magic=100, position_id=0, position_by_id=0, reason=3, volume_initial=0.03, volume_current=0.03, price_open=59000.0, sl=0.0, tp=0.0, price_current=62988.01, price_stoplimit=0.0, symbol='BTCUSD', comment='limit order', external_id='')
    '''
    logging.info(f'get_order_by_ticket: ticket={ticket}\n\r{order}, {mt5.last_error()}')

    order_dict = order[0]._asdict()
    order_dict['time_setup'] = utc_from_timestamp(order[0].time_setup)
    order_dict['time_setup_msc'] = utc_from_timestamp(order[0].time_setup_msc)
    logging.info(f'get_order_by_ticket: ticket={ticket}\n\r{order_dict}, {mt5.last_error()}')
    
    return order_dict


def get_orders(symbol):
    orders = mt5.orders_get(symbol=symbol)
    if orders is None:
        logging.warning(f"get_orders: No orders on {symbol}, error code={mt5.last_error()}") 
        return None

    n = 0
    count = len(orders)

    orders_dict = {}
    orders_dict['count'] = count
    orders_dict['orders'] = [order._asdict() for order in orders]

    for order in orders_dict['orders']:
        order['time_setup']= utc_from_timestamp(order['time_setup'])
        order['time_setup_msc']= utc_from_timestamp(order['time_setup_msc'])
        '''
        OrderSendResult(retcode=10009, deal=0, order=47247595, volume=0.05, price=0.0, bid=65348.46, ask=65380.340000000004, comment='limit order', request_id=3922353979, retcode_external=0, request=TradeRequest(action=5, magic=0, order=0, symbol='BTCUSD', volume=0.05, price=59000.0, stoplimit=0.0, sl=0.0, tp=0.0, deviation=0, type=2, type_filling=2, type_time=0, expiration=0, comment='limit order', position=0, position_by=0))
        '''
        n += 1
        logging.info(f'get_orders[{n}/{count}]: {order}')
    logging.info(f'get_orders: {orders}, {mt5.last_error()}')
    logging.info(f'get_orders: {orders_dict}, {mt5.last_error()}')
    return orders_dict


if __name__ == '__main__':
    init()

    # account
    ## [x] get_account_info()


    # order
    ## [x] market_order('BTCUSD', 0.03, 'buy')  
    ## [x] limit_order('BTCUSD', 'buy', volume=0.05, price=59000)
    ## [x] modify_order_by_price(ticket=47106125, price=63000)
    ## [x] delete_order(ticket=47106125)


    # symbols
    ## [x] get_all_symbols()
    ## [x] get_symbol_info('BTCUSD')


    # list orders
    ## [x] 
    get_orders('BTCUSD')
    ## [x] get_order_by_ticket(ticket=47247319)


    # position
    # [x] close_position_by_volume(ticket=47106357, volume=0.01)
    # [x] close_position(ticket=47086921)
    # [ ] close_all_positions(symbol='BTCUSD')
    # [x] get_all_positions(symbol='BTCUSD')
    # [x] get_position(47106361)

    mt5.shutdown()
