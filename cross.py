#!/usr/bin/env python

import logging
import time

import schedule
from talib import EMA

from common import API, SIZE, Base, cross_up, cross_down

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

            logging.info('symbol=%s, time=%s', symbol, t)

            if cross_up(ema6, ema18):
                logging.info('buy %s', symbol)
            elif cross_down(ema6, ema18):
                logging.info('sell %s', symbol)
                units = -units
            else:
                continue

            response = API.order.market(
                ACCOUNT_ID,
                instrument=symbol,
                units=units
            )
            if response.status != 201:
                print(response.body)


if __name__ == '__main__':
    cross = Cross()
    schedule.every(10).seconds.do(cross.data)
    schedule.every(5).seconds.do(cross.process)
    while True:
        schedule.run_pending()
        time.sleep(1)
