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


def process():
    logging.info('process')
    for i in instruments:
        i.data = alpaca.get_quotes(i.symbol)
        i.quantity = int(ORDER_SIZE / i.data['close'][-1])
        i.cci = TA.CCI(i.data, period=28)
        price = i.data['close'][-1]
        if i.cci[-2] < 0 < i.cci[-1]:
            logging.info('Buy: symbol={}, price={}'.format(i.symbol, price))
            if i.short:
                td.order(i, td.SELL)
                i.short = False
            td.order(i, td.BUY)
            i.long = True
        elif i.cci[-2] > 0 > i.cci[-1]:
            logging.info('Sell: symbol={}, price={}'.format(i.symbol, price))
            if i.long:
                td.order(i, td.BUY)
                i.long = False
            td.order(i, td.SELL)
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
