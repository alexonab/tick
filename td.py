import logging
import time

import pandas as pd
import requests

BASE_URL = 'https://api.tdameritrade.com/v1'
CLIENT_ID = 'ULGR9QXGJPZMHTHHFJDM8SC7XLBKLNQZ'
TOKENS = {
    'refresh': 'AyOY0iZMmi/ZHxVtL1cUZ8R+CzwVPGZE5SjSeSyq6WOn/i8mvUKDydCa3oumQxRx8jVKWIvR4kghdty5nuFgBGesSYDKw6COU6s/HfN6ZQgyv6CsIgZfk08JoqN1DkAFc2gKqhTeyd2J/39WY/nnXA0i+ODAoBROy5W6mDgF5xslFFx7bWAaMl5+PgFVy+jjltl66ayFzgtMZANGj79df9f+meSF27UgrWnO0guwLPWMsWAf/1ms6dpU+RDAZ90DCHslMGNa3C9r0rLKiOkG7HnT9DUFCG1WAuqtrb6b6rr6DpdQP1OTiAsIeKnW4BRND2qQrcSkEcVwKZlCsOm88AqldGexK8tCd2OPp/VWUN5Ry+X0sGcuXQ6Lx1rmIQ+2yC/PqCVZKy9ZlwVS52EvmB04pDdJBnWFehsbgo6NEF5a16rkpCc1/F/BjJL100MQuG4LYrgoVi/JHHvlrcneylBYO/Am3oecLrSYoMY6KKM6Fx1OEmsE/vp6UDl5RVHt6a+F1QI0Jh4IT19EiMTVXSTeCP/Z68KDYJZRLd1j4zNvmpFXHgxdyvJARxpEyVhRPRQyR6XjHAk5fVAbMb1SYXrMa/Z1h3YbUchBAZwWUnjStw/b16GQWqbKl5loNm6xEyClUiLSHG2IbjV92FqTvEF/yJVVtSYhKgZ/VTV1c7Lv5eeljhP9ixas+jMdSP26GG/jeJPekxi6m0Lqakx0Lo16it2HXg18Yz9Fat/oLFEikxk0GmJPWE8S37U6SKOXajdLpgEJEqiUTapoYAF7seJNVSNuxHvaQutlDGXXiLQclnIR+iM+gvzWIE/VlYfTCdD3Y4aj9p7DQZJxDd9dMqg96D6WWVrtcY2KlIlLcboD2l6EyjX2VTRJ54en5Nyyyl16R/AteGc=212FD3x19z9sWBHDJACbC00B75E',
    'refresh_expiry': 0,
    'access': '',
    'access_expiry': 0
}
ACCOUNT_ID = '865375237'
# ACCOUNT_ID = 'D-13215500'
BUY = 'Buy'
SELL = 'Sell'


def headers():
    return {'Authorization': 'Bearer {}'.format(get_token())}


def get_token():
    t = time.time() + 60
    # TODO: Use following when you are able to pickle the refresh token
    # if t > TOKENS['refresh_expiry'] or t > TOKENS['access_expiry']:
    # 'access_type': 'offline',
    # TOKENS['refresh'] = j['refresh_token']
    # TOKENS['refresh_expiry'] = t + j['refresh_token_expires_in']
    if t > TOKENS['access_expiry']:
        r = requests.post(BASE_URL + '/oauth2/token', data={
            'grant_type': 'refresh_token',
            'refresh_token': TOKENS['refresh'],
            'client_id': CLIENT_ID
        })
        j = r.json()
        t = time.time()
        TOKENS['access'] = j['access_token']
        TOKENS['access_expiry'] = t + j['expires_in']
    return TOKENS['access']


def get_account():
    r = requests.get(BASE_URL + '/accounts/{}'.format(ACCOUNT_ID), headers=headers())
    print(r.content)


def get_price_history(symbol, frequency_type='minute', frequency=1):
    r = requests.get(BASE_URL + '/marketdata/{}/pricehistory'.format(symbol), headers=headers(), params={
        'period': 1,
        'frequencyType': frequency_type,
        'frequency': frequency,
        'needExtendedHoursData': False
    })
    j = r.json()
    candles = j['candles']
    records = [
        {'time': pd.to_datetime(c['datetime'], unit='ms'), 'open': c['open'], 'high': c['high'],
         'low': c['low'], 'close': c['close'], 'volume': c['volume']} for c in candles]
    return pd.DataFrame.from_records(records, index='time')


def buy(instrument):
    _order(instrument, BUY)
    instrument.position = True


def sell(instrument):
    _order(instrument, SELL)
    instrument.position = True


def _order(instrument, instruction):
    logging.info('{}: symbol={}'.format(instruction, instrument.symbol))
    q = instrument.quantity
    if instrument.position:
        q *= 2
    r = requests.post(BASE_URL + '/accounts/{}/orders'.format(ACCOUNT_ID), headers=headers(), json={
        'orderType': 'MARKET',
        'session': 'NORMAL',
        'duration': 'DAY',
        'orderStrategyType': 'SINGLE',
        'orderLegCollection': [
            {
                'instruction': instruction,
                'quantity': q,
                'instrument': {
                    'symbol': instrument.symbol,
                    'assetType': 'EQUITY'
                }
            }
        ]
    })
    print(r)
