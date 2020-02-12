import alpaca_trade_api as tradeapi
import pandas as pd

ID = 'AK0R33BX16GW5R5Q7NOX'
SECRET = '7MlM7hCShyAV6Jmn0QyaRVE0OLf9Hrhg0LOxRUYd'
API = tradeapi.REST(ID, SECRET, api_version='v2')


def heikin_ashi(data: pd.DataFrame):
    data.close = (data.open + data.close + data.high + data.low) / 4
    _open = [(data.open[0] + data.close[0]) / 2]
    [_open.append((_open[i] + data.close[i]) / 2) for i in range(0, len(data) - 1)]
    data.open = _open
    data.high = data[['open', 'close', 'high']].max(axis=1)
    data.low = data[['open', 'close', 'low']].min(axis=1)
    return data


def get_bars(symbols, interval='1Min', limit=100):
    bars = API.get_barset(symbols, interval, limit).df
    for s in symbols:
        b = bars[s]
        b_ha = heikin_ashi(bars[s].copy())
        bars[s] = heikin_ashi(bars[s])
    return bars


if __name__ == '__main__':
    get_bars(['AAPL'])
