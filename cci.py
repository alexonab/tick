#!/usr/bin/env python

import logging

from finta import TA

import alpaca
import td

LENGTH = 8


def process(i: alpaca.Instrument):
    logging.info('processing {}'.format(i.symbol))
    i.cci = TA.CCI(i.heikins, period=i.length)
    print(i.heikins.index[-1], i.heikins.close[-1], i.cci[-2], i.cci[-1])
    q = i.quantity
    if i.long or i.short:
        q *= 2
    if i.cci[-2] < 0 < i.cci[-1]:
        if not i.long:
            td.order(i, td.BUY, q)
            i.long = True
            i.short = False
    elif i.cci[-2] > 0 > i.cci[-1]:
        if not i.short:
            td.order(i, td.SELL, q)
            i.short = True
            i.long = False


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
    # instruments.append(Instrument('AMZN', 25))
    # instruments.append(Instrument('AAPL', 150))
    # instruments.append(Instrument('NFLX', 150))

    # schedule.every(15).seconds.do(process)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
