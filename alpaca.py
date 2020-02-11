import alpaca_trade_api as tradeapi

ID = 'AK0R33BX16GW5R5Q7NOX'
SECRET = '7MlM7hCShyAV6Jmn0QyaRVE0OLf9Hrhg0LOxRUYd'
API = tradeapi.REST(ID, SECRET, api_version='v2')


def get_bars(symbols, interval='1Min'):
    return API.get_barset(symbols, interval).df
