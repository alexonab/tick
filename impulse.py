#!/usr/bin/env python

import logging
import time

import schedule
from talib import EMA
from v20 import transaction

from common import SYMBOLS, API, SIZE, PROFIT, LOSS, DELTA, Base, cross_up, \
    cross_down

# API = Context(
#     'api-fxpractice.oanda.com',
#     token='d9239a7c4e8dcad5d6c70ed6769e81e9-6f3637c29d8583d11f1336a9788071b4'
# )
# ACCOUNT_ID = '101-001-13004448-001'
# SIZE = 100000

# RESOLUTION = 'M1'
# PROFIT = 4.5
# LOSS = 3
# MARGIN = 0.25
ACCOUNT_ID = '001-001-3420740-003'


class Impulse(Base):
    def process(self):
        logging.info('process')

        # Open positions
        response = API.position.list_open(ACCOUNT_ID)
        if response.status != 200:
            print(response.body)
        positions = set([p.instrument for p in response.body['positions']])

        # Pending orders
        response = API.order.list_pending(ACCOUNT_ID)
        if response.status != 200:
            print(response.body)
        orders = [o for o in filter(
            lambda o: o.type in ['STOP', 'LIMIT'], response.body['orders'])]
        for o in orders:
            positions.add(o.instrument)

        # Prices
        response = API.pricing.get(ACCOUNT_ID, instruments=','.join(SYMBOLS))
        prices = response.body['prices']

        # Order
        for i, instrument in enumerate(self.instruments):
            symbol = instrument.symbol
            if symbol in positions:
                continue
            data = instrument.data
            t = data['time'].values[-1]
            close = data['close'].values
            ema6 = EMA(close, timeperiod=6)
            ema18 = EMA(close, timeperiod=18)
            units = SIZE
            buy = False
            ask = prices[i].asks[0].price
            bid = prices[i].bids[0].price
            price = ask

            logging.info('symbol=%s, time=%s, ask=%.5f, bid=%.5f', symbol, t, ask, bid)

            if cross_up(ema6, ema18):
                logging.info('buy %s', symbol)
                buy = True
            elif cross_down(ema6, ema18):
                logging.info('sell %s', symbol)
                price = bid
                units = -units
            else:
                continue

            response = API.order.stop(
                ACCOUNT_ID,
                instrument=symbol,
                units=units,
                price=instrument.price_value(
                    price + instrument.pips_value(DELTA, buy)),
                takeProfitOnFill=transaction.TakeProfitDetails(
                    price=instrument.price_value(price + instrument.pips_value(PROFIT, buy))),
                stopLossOnFill=transaction.StopLossDetails(
                    price=instrument.price_value(price - instrument.pips_value(LOSS, buy))),
                timeInForce='GTD',
                gtdTime=str(time.time() + 60)
            )
            if response.status != 201:
                print(response.body)


if __name__ == '__main__':
    impulse = Impulse()
    schedule.every(10).seconds.do(impulse.data)
    schedule.every(5).seconds.do(impulse.process)
    while True:
        schedule.run_pending()
        time.sleep(1)
