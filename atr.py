#!/usr/bin/env python
import logging

from finta import TA

import alpaca
import td


class Instrument(alpaca.Instrument):
    def __init__(self, symbol, quantity, length, multiplier):
        super.__init__(symbol, quantity, length)
        self.multiplier = multiplier


def process(self, instrument: Instrument):
    data = instrument.heikins
    atr = TA.ATR(data, instrument.length)

    # Long
    stops = (data.high + data.low - atr) / 2
    long_stop = stops[0]
    for i in range(1, len(stops) - 1):
        if data.close[i] > long_stop:
            long_stop = max(long_stop, stops[i])

    # Stop
    stops = (data.high + data.low + atr) / 2
    short_stop = stops[0]
    for i in range(1, len(stops) - 1):
        if data.close[i] < short_stop:
            short_stop = min(short_stop, stops[i])

    # Signal
    q = instrument.quantity
    if instrument.long or instrument.short:
        q *= 2
    if not instrument.long and short_stop < data.close[0] < long_stop:
        td.order(instrument, td.BUY, q)
        instrument.long = True
        instrument.short = False
    elif long_stop > data.close[0] > short_stop:
        td.order(instrument, td.SELL, q)
        instrument.short = True
        instrument.long = False


if __name__ == '__main__':
    # Logging
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
    logging.getLogger('schedule').propagate = False

    # Stocks
    instruments.append(Instrument('AMZN', 25))
    instruments.append(Instrument('AAPL', 150))
    instruments.append(Instrument('NFLX', 150))
