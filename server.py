from aiohttp import web

routes = web.RouteTableDef()


def cci(i):
    pass


@routes.post('/ddyNVCYhOlZkAdEJXAQNmnFQQuWyjLXH')
async def hello(request: web.Request):
    return web.Response(status=204)


app = web.Application()
app.add_routes(routes)
web.run_app(app)
