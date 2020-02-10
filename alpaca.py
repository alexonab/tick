import alpaca_trade_api as tradeapi
import pandas as pd

ID = 'AK0R33BX16GW5R5Q7NOX'
SECRET = '7MlM7hCShyAV6Jmn0QyaRVE0OLf9Hrhg0LOxRUYd'
API = tradeapi.REST(ID, SECRET, api_version='v2')


def get_quotes(symbol, interval='1min'):
    quotes = API.alpha_vantage.intraday_quotes(symbol, interval=interval)
    records = [
        {'time': pd.to_datetime(c['datetime'], unit='ms'), 'open': c['open'], 'high': c['high'],
         'low': c['low'], 'close': c['close'], 'volume': c['volume']} for c in candles]
    return pd.DataFrame.from_records(records, index='time')
    return API.alpha_vantage.intraday_quotes(symbol, interval=interval)


if __name__ == '__main__':
    quotes = get_quotes('AAPL')
