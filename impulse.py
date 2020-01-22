#!/usr/bin/env python

import logging
import time

import pandas as pd
import schedule
from talib import EMA
from v20 import Context, transaction

SYMBOLS = [
    'AUD_CAD',
    'AUD_JPY',
    'AUD_USD',
    'CAD_JPY',
    'EUR_AUD',
    'EUR_CAD',
    'EUR_CHF',
    'EUR_JPY',
    'EUR_USD',
    'GBP_USD',
    'HKD_JPY',
    'USD_CAD',
    'USD_CHF',
    'USD_HKD',
    'USD_JPY'
]
# API = Context(
#     'api-fxpractice.oanda.com',
#     token='d9239a7c4e8dcad5d6c70ed6769e81e9-6f3637c29d8583d11f1336a9788071b4'
# )
# ACCOUNT_ID = '101-001-13004448-001'
# SIZE = 100000

# Live
API = Context(
    'api-fxtrade.oanda.com',
    token='a773e0c5b6a682afa486d77beb884fc1-4823f26d2d2f72cba25c59626caacb54'
)
ACCOUNT_ID = '001-001-3420740-003'
SIZE = 5000

RESOLUTION = 'M5'
PROFIT = 9
LOSS = 6
MARGIN = 0.5

# RESOLUTION = 'M1'
# PROFIT = 4.5
# LOSS = 3
# MARGIN = 0.25


def cross_up(series1, series2):
    return series1[-2] < series2[-2] and series1[-1] > series2[-1]


def cross_down(series1, series2):
    return series1[-2] > series2[-2] and series1[-1] < series2[-1]


class Instrument:
    def __init__(self, symbol):
        self.symbol = symbol
        self.data = None
        self.since = None

    def pips_value(self, pips, buy):
        value = pips / 10000
        if 'JPY' in self.symbol:
            value = pips / 100
        if not buy:
            return -value
        return value

    def price_value(self, price):
        if 'JPY' in self.symbol:
            return "{:.3f}".format(price)
        else:
            return "{:.5f}".format(price)


class Impulse:
    def __init__(self):
        self.instruments = []
        for symbol in SYMBOLS:
            self.instruments.append(Instrument(symbol))
        self.data()

    def data(self):
        logging.info('data')
        for instrument in self.instruments:
            from_time = instrument.since
            include_first = None
            if from_time is not None:
                include_first = False

            # Candles
            response = API.instrument.candles(instrument.symbol, granularity=RESOLUTION, fromTime=from_time,
                                              includeFirst=include_first)
            # candles = [c for c in filter(lambda c: c.complete, response.body['candles'])]
            candles = response.body['candles']
            records = [
                {'time': pd.to_datetime(c.time), 'open': c.mid.o, 'high': c.mid.h,
                 'low': c.mid.l, 'close': c.mid.c, 'volume': c.volume} for c in candles]
            if len(records) == 0:
                continue
            data = pd.DataFrame.from_records(records)
            if instrument.data is None:
                instrument.data = data
            else:
                instrument.data = instrument.data.append(data)[len(records):]
            instrument.since = candles[-1].time

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

            logging.info('symbol=%s, time=%s, ask=%.5f, bid=%.5f',
                         symbol, t, ask, bid)
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
                    price + instrument.pips_value(MARGIN, buy)),
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
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
    logging.getLogger('schedule').propagate = False
    i = Impulse()
    schedule.every(10).seconds.do(i.data)
    schedule.every(5).seconds.do(i.process)
    while True:
        schedule.run_pending()
        time.sleep(1)
