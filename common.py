import logging

import pandas as pd
from v20 import Context

API = Context(
    'api-fxtrade.oanda.com',
    token='a773e0c5b6a682afa486d77beb884fc1-4823f26d2d2f72cba25c59626caacb54'
)
SIZE = 5000
RESOLUTION = 'M5'
PROFIT = 9
LOSS = 6
DELTA = 0.5
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


class Base:
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


# Logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.getLogger('schedule').propagate = False
