from backtesting import Backtest, Strategy
from finta import TA

import alpaca


class CCI(Strategy):
    def init(self):
        self.cci = self.I(TA.CCI, data, 28)

    def next(self):
        if self.cci[-2] < 0 < self.cci[-1]:
            self.buy()
        elif self.cci[-2] > 0 > self.cci[-1]:
            self.sell()


data = alpaca.get_bars(['MSFT'], interval='1Min', limit=1000)
data = data['MSFT'].dropna()
data['Open'] = data['open']
data['High'] = data['high']
data['Low'] = data['low']
data['Close'] = data['close']
data['Volume'] = data['volume']
bt = Backtest(data, CCI, cash=1000000)

bt.run()
bt.plot()
