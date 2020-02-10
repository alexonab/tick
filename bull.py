#!/usr/bin/env python

import logging
import time
from datetime import datetime, timedelta

import numpy as np

from common import SIZE, Base

# ACCOUNT_ID = '101-001-13004448-001'
ACCOUNT_ID = '001-001-3420740-004'


class Bull(Base):
    @staticmethod
    def uptrend(data):
        n = -30
        ema6 = data['ema6'][n:]
        ema18 = data['ema18'][n:]
        ema50 = data['ema50'][n:]
        sma200 = data['sma200'][n:]
        adx = data['adx'][-1]
        return np.all(ema6 > ema18) and np.all(ema18 > ema50) and np.all(ema50 > sma200) and adx > 25

    def process(self, index=None):
        # logging.info('process')

        # Open trades
        # response = API.trade.list_open(ACCOUNT_ID)
        # trades = [Trade(t.id, t.instrument, True if t.initialUnits > 0 else False)
        #           for t in response.body['trades']]

        # Scan
        for instrument in self.instruments:
            symbol = instrument.symbol
            data = instrument.dataM15[:index]
            i = instrument.dataH1.index <= data.index[-1].replace(microsecond=0, second=0, minute=0)
            dataH1 = instrument.dataH1[i]
            time = data.index[-1]
            high = data['high']
            units = SIZE

            # Uptrend M15
            n = -25
            ema6 = data['ema6'][n:]
            ema18 = data['ema18'][n:]
            ema50 = data['ema50'][n:]
            sma200 = data['sma200'][n:]
            adx = data['adx'][-1]
            if not (np.all(ema6 > ema18) and np.all(ema18 > ema50) and np.all(ema50 > sma200) and adx > 25):
                continue

            logging.

            # # Uptrend H1
            # n = -10
            # ema6 = dataH1['ema6'][n:]
            # ema18 = dataH1['ema18'][n:]
            # ema50 = dataH1['ema50'][n:]
            # if not (np.all(ema6 > ema18) and np.all(ema18 > ema50) and adx > 25):
            #     continue

            bull.trends += 1

            # Identify candles
            i = np.argmax(np.flip(high[:-1].values < high[1:].values))
            if i == 0:
                continue
            corrective = data[-i:]
            j = np.argmax(np.flip(high[:-1].values > high[1:].values)) + i
            if j == 0:
                continue
            impulsive = data[-j:-i]

            # Validation - start
            # Min length of corrective and impulsive candles
            if len(corrective) < 1 or len(impulsive) < 2:
                continue

            # All corrective candles's (but last) low is above ema6
            if not np.all(corrective['high'][:-1] > corrective['ema6'][:-1]):
                continue

            # Last corrective candle's high > ema6 and low < ema6
            if not corrective['high'][-1] > corrective['ema6'][-1] \
                    and corrective['low'][-1] < corrective['ema6'][-1]:
                continue

            # Low of the last corrective candle > low of the first impulsive candle
            if not corrective['low'][-1] > impulsive['low'][0]:
                continue

            # - If an open order exists cancel it
            # Validation - end

            # Order
            logging.info('order symbol=%s, time=%s', symbol, time)
            bull.orders += 1
            # Buy stop order at high of the last corrective candle + spread

            # TODO: Cancel order in case they are not triggered on time


if __name__ == '__main__':
    bull = Bull()
    # schedule.every(10).seconds.do(bull.data)
    # schedule.every(5).seconds.do(bull.process)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
    t = str((datetime.now() - timedelta(days=10)).timestamp())
    for instrument in bull.instruments:
        instrument.sinceM15 = t
        instrument.sinceH1 = t
    bull.data()
    bull.trends = 0
    bull.orders = 0
    instrument = bull.instruments[0]
    for i in range(len(instrument.dataM15[1:])):
        bull.process(-i - 1)
        # logging.info(bull.instruments[0].dataM15.index[-i - 1], trends)
    print(instrument)
