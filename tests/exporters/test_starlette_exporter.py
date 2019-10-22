import pytest
from starlette.applications import Starlette
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import PlainTextResponse
from starlette.testclient import TestClient

from urouter.constants import Method as mt
from urouter.exporters.starlette_exporter import StarletteRouter


def make_request_factory(value):
    async def handler(request):
        return PlainTextResponse(content=value)

    return handler


def test_method_not_implement():
    app = Starlette()
    router = StarletteRouter(app)

    async def handle(request):
        return PlainTextResponse()

    with pytest.raises(TypeError):
        router.handle("/h", handle)


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
def test_route_methods(method, pattern):
    app = Starlette()
    router = StarletteRouter(app)
    http_method = getattr(router, method.lower())
    http_method(pattern, make_request_factory(method))

    router.export()

    client = TestClient(app)
    caller = getattr(client, method.lower())
    resp = caller(pattern)
    assert resp.status_code == 200
    assert resp.text == method


def test_route_mount():
    app = Starlette()
    router = StarletteRouter(app)

    router.get("/hello", make_request_factory("hello"))

    sub_router = router.make_router()
    sub_router.get("/sub-hello", make_request_factory("hello"))

    router.mount("/sub/", sub_router)
    router.export()

    client = TestClient(app)

    resp = client.get("/hello")
    assert resp.status_code == 200
    assert resp.text == "hello"

    resp = client.get("/sub/sub-hello")
    assert resp.status_code == 200
    assert resp.text == "hello"


def test_route_use_middleware():
    class ExampleMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request, call_next):
            response = await call_next(request)
            response.headers["m1"] = "Example"
            return response

    class InfoMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request, call_next):
            response = await call_next(request)
            response.headers["m2"] = "info"
            return response

    class CustomMiddleware3(BaseHTTPMiddleware):
        async def dispatch(self, request, call_next):
            response = await call_next(request)
            response.headers["m3"] = "inline"
            return response

    async def handler(request):
        return PlainTextResponse(content="test")

    app = Starlette()
    example_middleware = ExampleMiddleware(app)
    info_middleware = InfoMiddleware(app)
    m3_middleware = CustomMiddleware3(app)
    r = StarletteRouter(app).use(example_middleware).use(info_middleware)
    r.include(m3_middleware).get("/hello", handler)
    r.export()
    client = TestClient(app)

    resp = client.get("/hello")
    assert resp.status_code == 200
    assert resp.headers["m1"] == "Example"
    assert resp.headers["m2"] == "info"
    assert resp.headers["m3"] == "inline"


def test_route_use_class_middleware():
    class ExampleMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request, call_next):
            response = await call_next(request)
            response.headers["m1"] = "Example"
            return response

    class InfoMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request, call_next):
            response = await call_next(request)
            response.headers["m2"] = "info"
            return response

    class CustomMiddleware3(BaseHTTPMiddleware):
        async def dispatch(self, request, call_next):
            response = await call_next(request)
            response.headers["m3"] = "inline"
            return response

    async def handler(request):
        return PlainTextResponse(content="test")

    app = Starlette()
    r = StarletteRouter(app).use(ExampleMiddleware).use(InfoMiddleware)
    r.include(CustomMiddleware3).get("/hello", handler)
    r.export()
    client = TestClient(app)

    resp = client.get("/hello")
    assert resp.status_code == 200
    assert resp.headers["m1"] == "Example"
    assert resp.headers["m2"] == "info"
    assert resp.headers["m3"] == "inline"


def test_route_inline_middleware():
    class ExampleMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request, call_next):
            response = await call_next(request)
            response.headers["m1"] = "Example"
            return response

    class InfoMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request, call_next):
            response = await call_next(request)
            response.headers["m2"] = "info"
            return response

    async def handler(request):
        return PlainTextResponse(content="Test")

    async def handler2(request):
        return PlainTextResponse(content="Test2")

    app = Starlette()

    example_middleware = ExampleMiddleware(app)
    info_middleware = InfoMiddleware(app)
    router = StarletteRouter(app).use(example_middleware)
    router.get("/hello", handler)
    router.include(info_middleware).get("/hello2", handler2)

    router.export()
    client = TestClient(app)

    resp = client.get("/hello")
    assert resp.status_code == 200
    assert resp.headers["m1"] == "Example"

    resp = client.get("/hello2")
    assert resp.status_code == 200
    assert resp.headers["m1"] == "Example"
    assert resp.headers["m2"] == "info"
