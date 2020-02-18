from backtesting import Backtest, Strategy

import engine
from atr import ATR
from finta import TA

class ATRTes(Strategy):
    def init(self):
        atr = self.multiplier * TA.ATR(candles, ).dropna()
    def next(self):

class BT(Strategy):
    strategy = None
    candles = None

    def init(self):
        self.sma1 = self.I(TA.SMA, candles, 10)

    def next(self):
        for i in self.strategy.instruments:
            i.process(self.candles, self)


if __name__ == '__main__':
    candles = engine.get_heikins('INTU')
    candles['Open'] = candles['open']
    candles['High'] = candles['high']
    candles['Low'] = candles['low']
    candles['Close'] = candles['close']
    candles['Volume'] = candles['volume']

    bt = Backtest(candles, BT, cash=1000000)
    bt.run(candles=candles, strategy=ATR())
    bt.plot()
