import pytest
from aiohttp import web

from urouter.constants import Method as mt
from urouter.exporters.aiohttp_exporter import AioHttpRouter


def make_request_factory(value):
    async def handler(request):
        return web.Response(text=value)

    return handler


@pytest.mark.parametrize(
    "method, pattern",
    [
        (mt.DELETE, "/delete"),
        (mt.GET, "/get"),
        (mt.OPTIONS, "/options"),
        (mt.PATCH, "/patch"),
        (mt.POST, "/post"),
        (mt.PUT, "/put"),
    ],
)
async def test_route_methods(method, pattern, aiohttp_client, loop):
    app = web.Application()
    router = AioHttpRouter(app)
    http_method = getattr(router, method.value.lower())
    http_method(pattern, make_request_factory(method.value))

    router.export()

    client = await aiohttp_client(app)
    caller = getattr(client, method.value.lower())
    resp = await caller(pattern)
    assert resp.status == 200
    text = await resp.text()
    assert text == method.value


@pytest.mark.parametrize(
    "method, pattern",
    [
        (mt.DELETE, "/delete"),
        (mt.GET, "/get"),
        (mt.OPTIONS, "/options"),
        (mt.PATCH, "/patch"),
        (mt.POST, "/post"),
        (mt.PUT, "/put"),
    ],
)
async def test_route_handle(method, pattern, aiohttp_client, loop):
    app = web.Application()
    router = AioHttpRouter(app)
    router.handle(pattern, make_request_factory(method.value))

    router.export()

    client = await aiohttp_client(app)
    caller = getattr(client, method.value.lower())
    resp = await caller(pattern)
    assert resp.status == 200
    text = await resp.text()
    assert text == method.value


async def test_route_mount(aiohttp_client, loop):
    app = web.Application()
    app["mws"] = []
    router = AioHttpRouter(app)

    router.get("/hello", make_request_factory("hello"))

    sub_router = router.make_router()
    sub_router.get("/sub-hello", make_request_factory("hello"))

    router.mount("/sub/", sub_router)
    router.export()

    client = await aiohttp_client(app)

    resp = await client.get("/hello")
    assert resp.status == 200
    text = await resp.text()
    assert text == "hello"

    resp = await client.get("/sub/sub-hello")
    assert resp.status == 200
    text = await resp.text()
    assert text == "hello"


async def test_route_use_middleware(aiohttp_client, loop):
    @web.middleware
    async def error_middleware(request, handler):
        request["m1"] = "error"
        response = await handler(request)
        return response

    @web.middleware
    async def info_middleware(request, handler):
        request["m2"] = "info"
        response = await handler(request)
        return response

    @web.middleware
    async def inline_middleware(request, handler):
        request["m3"] = "inline"
        response = await handler(request)
        return response

    async def handler(request):
        text = "{}_{}_{}".format(request["m1"], request["m2"], request["m3"])
        return web.Response(text=text)

    app = web.Application()
    r = AioHttpRouter(app).use(error_middleware).use(info_middleware)
    r.include(inline_middleware).get("/hello", handler)
    r.export()
    client = await aiohttp_client(app)

    resp = await client.get("/hello")
    assert resp.status == 200
    text = await resp.text()
    assert text == "error_info_inline"


async def test_route_inline_middleware(aiohttp_client, loop):
    @web.middleware
    async def error_middleware(request, handler):
        request["m1"] = "error"
        response = await handler(request)
        return response

    @web.middleware
    async def info_middleware(request, handler):
        request["m2"] = "info"
        response = await handler(request)
        return response

    async def handler(request):
        text = "{}_{}".format(request["m1"], request["m2"])
        return web.Response(text=text)

    app = web.Application()
    router = AioHttpRouter(app).use(error_middleware).use(info_middleware)
    router.get("/hello", handler)
    router.export()
    client = await aiohttp_client(app)

    resp = await client.get("/hello")
    assert resp.status == 200
    text = await resp.text()
    assert text == "error_info"
