from aiohttp import web

routes = web.RouteTableDef()


def cci(i):
    if i.long or i.short:
        q *= 2
    if i.cci[-2] < 0 < i.cci[-1]:
        if not i.long:
            td.order(i, td.BUY, q)
            i.long = True
    elif i.cci[-2] > 0 > i.cci[-1]:
        if not i.short:
            td.order(i, td.SELL, q)
            i.short = True

@routes.post('/ddyNVCYhOlZkAdEJXAQNmnFQQuWyjLXH')
async def hello(request: web.Request):

    return web.Response(status=204)


app = web.Application()
app.add_routes(routes)
web.run_app(app)
