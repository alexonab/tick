#!/usr/bin/env python

import logging
import time

import schedule
from talib import EMA

from common import API, SIZE, Base, Trade, cross_up, cross_down

ACCOUNT_ID = '001-001-3420740-004'


class Cross(Base):
    def process(self):
        logging.info('process')

        # Pending orders
        response = API.order.list_pending(ACCOUNT_ID)
        if response.status != 200:
            print(response.body)
        orders = [o.instrument for o in filter(
            lambda o: o.type in ['STOP', 'LIMIT'], response.body['orders'])]

        # Open trades
        response = API.trade.list_open(ACCOUNT_ID)
        trades = [Trade(t.id, t.instrument, True if t.initialUnits > 0 else False)
                  for t in response.body['trades']]

        # Order
        for instrument in self.instruments:
            symbol = instrument.symbol
            if symbol in orders:
                continue
            data = instrument.data
            t = data['time'].values[-1]
            close = data['close'].values
            ema6 = EMA(close, timeperiod=6)
            ema18 = EMA(close, timeperiod=18)
            units = SIZE
            buy = True

            logging.info('symbol=%s, time=%s', symbol, t)

            if cross_up(ema6, ema18):
                logging.info('buy %s', symbol)
            elif cross_down(ema6, ema18):
                logging.info('sell %s', symbol)
                buy = False
                units = -units
            else:
                continue

            # Close
            for trade in trades:
                if trade.symbol == symbol and trade.long == buy:
                    API.trade.close(ACCOUNT_ID, trade.id)

            # Order
            response = API.order.market(
                ACCOUNT_ID,
                instrument=symbol,
                units=units
            )


if __name__ == '__main__':
    cross = Cross()
    schedule.every(10).seconds.do(cross.data)
    schedule.every(5).seconds.do(cross.process)
    while True:
        schedule.run_pending()
        time.sleep(1)
