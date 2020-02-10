import logging

import pandas as pd
from talib import EMA, SMA, ADX
from v20 import Context

# API = Context(
#     'api-fxpractice.oanda.com',
#     token='d9239a7c4e8dcad5d6c70ed6769e81e9-6f3637c29d8583d11f1336a9788071b4'
# )
API = Context(
    'api-fxtrade.oanda.com',
    token='a773e0c5b6a682afa486d77beb884fc1-4823f26d2d2f72cba25c59626caacb54'
)
SIZE = 5000
RESOLUTION = 'M15'
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
    'NZD_USD',
    'USD_CAD',
    'USD_CHF',
    'USD_JPY'
]


def cross_up(series1, series2):
    return series1[-2] < series2[-2] and series1[-1] > series2[-1]


def cross_down(series1, series2):
    return series1[-2] > series2[-2] and series1[-1] < series2[-1]


class Instrument:
    def __init__(self, symbol):
        self.symbol = symbol
        self.dataM15 = None
        self.dataH1 = None
        self.sinceM15 = None
        self.sinceH1 = None

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


class Trade:
    def __init__(self, id, symbol, long):
        self.id = id
        self.symbol = symbol
        self.long = long


class Base:
    def __init__(self):
        self.instruments = []
        for symbol in SYMBOLS:
            self.instruments.append(Instrument(symbol))

    def data(self):
        for resolution in ['M15', 'H1']:
            logging.info('data resolution=%s', resolution)
            for instrument in self.instruments:
                from_time = getattr(instrument, 'since' + resolution)
                include_first = None
                if from_time is not None:
                    include_first = False

                # Candles
                response = API.instrument.candles(instrument.symbol, granularity=resolution, fromTime=from_time,
                                                  includeFirst=include_first)
                # candles = [c for c in filter(lambda c: c.complete, response.body['candles'])]
                candles = response.body['candles']
                records = [
                    {'time': pd.to_datetime(c.time), 'open': c.mid.o, 'high': c.mid.h,
                     'low': c.mid.l, 'close': c.mid.c, 'volume': c.volume} for c in candles]
                if len(records) == 0:
                    continue
                data = pd.DataFrame.from_records(records, index='time')
                key = 'data' + resolution
                if getattr(instrument, key) is None:
                    setattr(instrument, key, data)
                else:
                    setattr(instrument, key, getattr(instrument, key).append(data)[len(records):])
                close = getattr(instrument, key)['close']
                setattr(instrument, key, getattr(instrument, key).assign(
                    ema6=EMA(close, timeperiod=6),
                    ema18=EMA(close, timeperiod=18),
                    ema50=EMA(close, timeperiod=50),
                    sma200=SMA(close, timeperiod=200),
                    adx=ADX(getattr(instrument, key)['high'], getattr(instrument, key)['low'], close, timeperiod=14)
                ))
                setattr(instrument, 'since' + resolution, candles[-1].time)


# Logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.getLogger('schedule').propagate = False
