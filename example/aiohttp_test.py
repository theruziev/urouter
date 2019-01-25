from aiohttp import web

from router.exporters.aiohttp_exporter import AioHttpRouter


async def hello(request):
    return web.Response(text="Hello, world")


@web.middleware
async def error_middleware(request, handler):
    print("error", flush=True)
    response = await handler(request)
    return response


@web.middleware
async def info_middleware(request, handler):
    print("info", flush=True)
    response = await handler(request)
    return response


app = web.Application()


router = AioHttpRouter(app).use(error_middleware)

user_router = AioHttpRouter(app).use(info_middleware)
user_router.get("hello-world", hello)

router.mount("/user", user_router)
router.export()

if __name__ == '__main__':
    web.run_app(app)
