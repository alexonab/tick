import alpaca_trade_api as tradeapi
import pandas as pd

ID = 'AK0R33BX16GW5R5Q7NOX'
SECRET = '7MlM7hCShyAV6Jmn0QyaRVE0OLf9Hrhg0LOxRUYd'
API = tradeapi.REST(ID, SECRET, api_version='v2')


# Heikin Ashi has a unique method to filter out the noise
# its open, close, high, low require a different calculation approach
# please refer to the website mentioned above
def heikin_ashi(df1):
    # df1.reset_index(inplace=True)

    df1.ha_close = (df1.open + df1.close + df1.high + df1.low) / 4

    # initialize heikin ashi open
    df1.ha_open = 0
    df1.ha_open = df1.open[0]

    for n in range(1, len(df1)):
        df1.at[n, 'ha_open'] = (df1['ha_open'][n - 1] + df1['ha_close'][n - 1]) / 2

    temp = pd.concat([df1['ha_open'], df1['ha_close'], df1['low'], df1['high']], axis=1)
    df1['ha_high'] = temp.apply(max, axis=1)
    df1['ha_low'] = temp.apply(min, axis=1)

    return df1


def get_bars(symbols, interval='1Min', limit=100):
    bars = API.get_barset(symbols, interval, limit).df
    for s in symbols:
        bars[s] = heikin_ashi(bars[s])
    return bars
