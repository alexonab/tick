import pandas as pd
from finta import TA

from common import I


class Instrument(I):
    def __init__(self, symbol, quantity, period, multiplier):
        self.multiplier = multiplier
        super().__init__(symbol, quantity, period)

    def process(self, data: pd.DataFrame):
        # Warm up
        if len(data) < self.period + 1:
            return

        # Data
        atr = self.multiplier * TA.ATR(data, self.period).dropna()
        data = data.iloc[-len(atr):]
        time = data.index[-1]
        close = data.close[-1]
        price = data.price[-1]

        # Long
        long_stops = ((data.high + data.low) / 2) - atr
        long_stop = long_stops[0]
        for i in range(1, len(long_stops)):
            if data.close[i] > long_stop:
                long_stop = max(long_stop, long_stops[i])
                long_stops[i] = long_stop

        # Stop
        short_stops = ((data.high + data.low) / 2) + atr
        short_stop = short_stops[0]
        for i in range(1, len(short_stops)):
            if data.close[i] < short_stop:
                short_stop = min(short_stop, short_stops[i])
                short_stops[i] = short_stop

        print(time, data.open[-1], data.high[-1], data.low[-1], close, long_stops[-1], short_stops[-1])

        # output_file("atr.html")
        # p = figure(title="simple line example", x_axis_label='x', y_axis_label='y')
        # p.line(data.index, short_stops, legend="Temp.", line_width=2)
        # show(p)

        # Signal
        # if short_stop < close:
        #     print(f'Buy: stock {self.symbol} @ {price} on {time}')
        #     # self.long = True
        #     # self.short = False
        #     # td.buy(self)
        # elif long_stop > close:
        #     print(f'Sell: stock {self.symbol} @ {price} on {time}')
        #     # self.short = True
        #     # self.long = False
        #     # td.sell(self)


class ATR:
    def __init__(self):
        self.instruments = [
            Instrument('INTU', 1, 24, 1)
        ]
