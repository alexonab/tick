#!/usr/bin/env python

import logging
import time

import schedule
from talib import EMA

from common import API, SIZE, Base, Trade, cross_up, cross_down

# ACCOUNT_ID = '101-001-13004448-001'
ACCOUNT_ID = '001-001-3420740-004'


class Cross(Base):
    def process(self):
        logging.info('process')

        # Open trades
        response = API.trade.list_open(ACCOUNT_ID)
        trades = [Trade(t.id, t.instrument, True if t.initialUnits > 0 else False)
                  for t in response.body['trades']]

        # Order
        for instrument in self.instruments:
            symbol = instrument.symbol
            data = instrument.data
            t = data['time'].values[-1]
            close = data['close'].values
            ema3 = EMA(close, timeperiod=3)
            ema6 = EMA(close, timeperiod=6)
            ema18 = EMA(close, timeperiod=18)
            units = SIZE
            trade = next((t for t in trades if t.symbol ==
                          symbol), Trade(0, symbol, None))
            buy = True

            # logging.info('symbol=%s, time=%s', symbol, t)

            # Enter long
            if cross_up(ema6, ema18) and trade.long in [None, False]:
                logging.info("long entry: symbol=%s", symbol)
                response = API.order.market(
                    ACCOUNT_ID,
                    instrument=symbol,
                    units=SIZE
                )

            # Exit long
            if cross_down(ema3, ema6) and trade.long:
                logging.info("long exit: symbol=%s", symbol)
                API.trade.close(ACCOUNT_ID, trade.id)

            # Enter short
            if cross_down(ema6, ema18) and trade.long in [None, True]:
                logging.info("short entry: symbol=%s", symbol)
                response = API.order.market(
                    ACCOUNT_ID,
                    instrument=symbol,
                    units=-SIZE
                )

            # Exit short
            if cross_up(ema3, ema6) and trade.long is False:
                logging.info("short exit: symbol=%s", symbol)
                API.trade.close(ACCOUNT_ID, trade.id)


if __name__ == '__main__':
    cross = Cross()
    schedule.every(10).seconds.do(cross.data)
    schedule.every(5).seconds.do(cross.process)
    while True:
        schedule.run_pending()
        time.sleep(1)
