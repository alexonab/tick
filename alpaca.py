#!/usr/bin/env python

import logging

import alpaca_trade_api as tradeapi
import pandas as pd
# from polygon import WebSocketClient, STOCKS_CLUSTER

ID = 'AK0R33BX16GW5R5Q7NOX'
SECRET = '7MlM7hCShyAV6Jmn0QyaRVE0OLf9Hrhg0LOxRUYd'
API = tradeapi.REST(ID, SECRET, api_version='v2')
POLYGON_KEY_ID = 'MUe6Ti7Lb__t4msf6AiAmf7FnJb9Nn7T8e7H9g'

instruments = []


class Instrument():
    def __init__(self, symbol, quantity=1, period=8):
        self.symbol = symbol
        self.period = period
        self.quantity = quantity
        self.position = False
        self.long = False
        self.short = False
        self.candles = pd.DataFrame(columns=['open', 'high', 'low', 'close', 'volume'])
        self.heikins = self.candles.copy()


# def on_message(message):
#     quotes = json.loads(message)
#     for q in quotes:
#         if q['ev'] != 'AM':
#             logging.info(q)
#             continue
#         i = next((i for i in instruments if i.symbol == q['sym']), None)
#         t = pd.to_datetime(q['s'], unit='ms')
#         i.candles.loc[t] = [q['o'], q['h'], q['l'], q['c'], q['v']]
#         # b = i.bars.iloc[-1]
#         # h = i.heikins
#         # h.open = (b.open + b.high + b.low + b.close) / 4
#         # TODO: Don't compute it every time
#         i.heikins = get_heikins(i.candles)
#         if len(i.heikins) >= cci.LENGTH:
#             cci.process(i)
#     # TODO: Pickle it


if __name__ == '__main__':
    # Logging
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
    logging.getLogger('schedule').propagate = False

    # Stocks
    instruments.append(Instrument('AMZN', 25))
    instruments.append(Instrument('AAPL', 150))
    instruments.append(Instrument('NFLX', 150))
    instruments.append(Instrument('AMD', 1000))
    instruments.append(Instrument('MU', 1000))

    # WS
    # ws = WebSocketClient(STOCKS_CLUSTER, POLYGON_KEY_ID, on_message)
    # ws.run_async()
    # ws.subscribe('AM.AAPL', 'AM.NFLX', 'AM.AMZN', 'AM.AMD', 'AM.MU')
