#!/usr/bin/env python

from aiohttp import web

import td


class Instrument():
    def __init__(self, symbol, quantity=1, length=8):
        self.symbol = symbol
        self.quantity = quantity
        self.position = False


instruments = {
    'AAPL': Instrument('AAPL', 15),
    'MU': Instrument('MU', 100),
    'NVDA': Instrument('NVDA', 20),
    'SHOP': Instrument('SHOP', 10)
}

routes = web.RouteTableDef()


@routes.post('/ddyNVCYhOlZkAdEJXAQNmnFQQuWyjLXH')
async def hello(request: web.Request):
    body = await request.json()
    i = instruments[body['symbol']]
    s = body['signal']
    q = i.quantity
    if i.position:
        q += i.quantity
    td.order(i, s, q)
    i.position = True
    return web.Response(status=204)


if __name__ == '__main__':
    app = web.Application()
    app.add_routes(routes)
    web.run_app(app)
