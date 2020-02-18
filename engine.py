#!/usr/bin/env python

import asyncio
import json
import logging
from datetime import datetime, timedelta

import aiohttp
import pandas as pd

from atr import ATR

POLYGON_URL = 'https://api.polygon.io/v2/aggs/ticker/{}/range/1/minute/{}/{}'
POLYGON_KEY = 'MUe6Ti7Lb__t4msf6AiAmf7FnJb9Nn7T8e7H9g'
STOCKS = [
    'AAPL',
    'FB',
    'GOOGL',
    'MSFT',
    'NFLX',
    'ROKU',
    'SHOP',
    'BABA',
    'INTU',
    'V',
    'MA',
    'XOM',
    'CVX',
    'KO',
    'PEP',
    'ADBE',
    'NVDA',
    'CRM',
    'TSLA',
    'F',
    'GM',
    'QCOM',
    'MMM',
    'CVS',
    'MS',
    'GS',
    'UBER',
    'LYFT',
    'WDAY',
    'BAC',
    'C',
    'VZ',
    'T',
    'CMCSA',
    'CL',
    'PG',
    'AMD',
    'TGT',
    'PG',
    'UPS',
    'FDX',
    'UAL',
    'LUV',
    'HD',
    'LOW'
]


def fetch_quotes():
    async def fetch(symbol):
        _from = (datetime.today() - timedelta(weeks=16)).strftime('%Y-%m-%d')
        to = datetime.today().strftime('%Y-%m-%d')
        params = {'apiKey': POLYGON_KEY}
        async with aiohttp.ClientSession() as session:
            async with session.get(POLYGON_URL.format(symbol, _from, to), params=params) as r:
                return await r.json()

    loop = asyncio.get_event_loop()
    coroutines = [fetch(s) for s in STOCKS]
    responses = loop.run_until_complete(asyncio.gather(*coroutines))
    quotes = []
    for response in responses:
        for r in response['results']:
            quotes.append({
                'time': datetime.fromtimestamp(r['t'] / 1000.0),
                'symbol': response['ticker'],
                'open': r['o'],
                'high': r['h'],
                'low': r['l'],
                'close': r['c'],
                'volume': r['v']
            })

    stocks = pd.DataFrame.from_records(quotes, index=['symbol', 'time'])
    stocks.to_pickle('/tmp/stocks')


def load_bars():
    bars = pd.read_pickle('/tmp/stocks')
    bars['price'] = bars.close
    return bars


def load_heikins(bars: pd.DataFrame):
    bars.close = (bars.open + bars.close + bars.high + bars.low) / 4
    _open = [(bars.open[0] + bars.close[0]) / 2]
    [_open.append((_open[i] + bars.close[i]) / 2) for i in range(0, len(bars) - 1)]
    bars.open = _open
    bars.high = bars[['open', 'close', 'high']].max(axis=1)
    bars.low = bars[['open', 'close', 'low']].min(axis=1)
    return bars


def on_message(message):
    quotes = json.loads(message)
    # for q in quotes:
    #     if q['ev'] != 'AM':
    #         logging.info(q)
    #         continue
    #     i = next((i for i in instruments if i.symbol == q['sym']), None)
    #     t = pd.to_datetime(q['s'], unit='ms')
    #     i.candles.loc[t] = [q['o'], q['h'], q['l'], q['c'], q['v']]
    #     # b = i.bars.iloc[-1]
    #     # h = i.heikins
    #     # h.open = (b.open + b.high + b.low + b.close) / 4
    #     # TODO: Don't compute it every time
    #     i.heikins = get_heikins(i.candles)
    #     if len(i.heikins) >= cci.LENGTH:
    #         cci.process(i)
    # TODO: Pickle it


def main():
    # Logging
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
    logging.getLogger('schedule').propagate = False

    # Fetch quotes
    # fetch_quotes()

    # bars = load_bars()
    # bars.where(bars["symbol"] == "INTU", inplace=True)
    # bars = bars.resample('1H').agg({
    #     'symbol': 'first',
    #     'open': 'first',
    #     'high': 'max',
    #     'low': 'min',
    #     'close': 'last',
    #     'volume': 'sum'}, inplace=True).dropna().
    # print(bars)
    simulate()

    # Socket
    # ws = WebSocketClient(STOCKS_CLUSTER, POLYGON_KEY, on_message)
    # ws.run_async()
    # ws.subscribe('AM.AAPL', 'AM.NFLX', 'AM.AMZN', 'AM.AMD', 'AM.MU')

    # print(
    #     f'On: {r.aggresponse} Apple opened at {resp.open} and closed at {resp.close}')
    # for s in SYMBOLS:
    #     fetch(s, '2020-02-01')


def simulate():
    atr = ATR()
    bars = load_bars()
    for instrument in atr.instruments:
        bars = bars.query('symbol == "{}"'.format(instrument.symbol))[-500:]
        bars = load_heikins(bars)
        bars['direction'] = 1
        # instrument.process(bars)
        for i in range(len(bars)):
            instrument.process(bars[:i + 1])


if __name__ == '__main__':
    main()
