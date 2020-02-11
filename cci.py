#!/usr/bin/env python

import logging
import time

import schedule
from finta import TA

import alpaca
import td

ORDER_SIZE = 1000

instruments = []


class Instrument():
    def __init__(self, symbol, length=28, middle=0):
        self.symbol = symbol
        self.length = length
        self.middle = middle
        self.quantity = 1
        self.long = False
        self.short = False


def process():
    logging.info('process')
    data = alpaca.get_bars([i.symbol for i in instruments])
    for i in instruments:
        i.data = data[i.symbol].dropna(subset=["open"])
        i.quantity = int(ORDER_SIZE / i.data['close'][-1])
        i.cci = TA.CCI(i.data, period=28)
        q = i.quantity
        if i.long or i.short:
            q *= 2
        if i.cci[-2] < 0 < i.cci[-1]:
            if not i.long:
                td.order(i, td.BUY, q)
                i.long = True
        elif i.cci[-2] > 0 > i.cci[-1]:
            if not i.short:
                td.order(i, td.SELL, q)
                i.short = True


if __name__ == '__main__':
    # Logging
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
    logging.getLogger('schedule').propagate = False

    # Futures
    # instruments.append(Instrument('/BTC'))
    # instruments.append(Instrument('/CL'))
    # instruments.append(Instrument('/ES'))
    # instruments.append(Instrument('/GC'))
    # instruments.append(Instrument('/M2K'))
    # instruments.append(Instrument('/PL'))
    # instruments.append(Instrument('/RTY'))
    # instruments.append(Instrument('/SI'))
    # instruments.append(Instrument('/XK'))
    # instruments.append(Instrument('/XW'))

    # Stocks
    instruments.append(Instrument('AAPL'))
    instruments.append(Instrument('ADBE'))
    # instruments.append(Instrument('AMZN'))
    instruments.append(Instrument('BABA'))
    instruments.append(Instrument('CRM'))
    # instruments.append(Instrument('GOOGL'))
    instruments.append(Instrument('FB'))
    instruments.append(Instrument('MSFT'))
    instruments.append(Instrument('NFLX'))
    instruments.append(Instrument('NVDA'))
    instruments.append(Instrument('XOP'))
    instruments.append(Instrument('QCOM'))
    instruments.append(Instrument('MMM'))

    schedule.every(15).seconds.do(process)
    while True:
        schedule.run_pending()
        time.sleep(1)
