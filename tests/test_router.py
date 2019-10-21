import pytest

from urouter.api import Route, Router
from urouter.constants import Method as mt


@pytest.mark.parametrize(
    "method, pattern, handler",
    [
        (mt.CONNECT, "/connect", lambda x: mt.CONNECT),
        (mt.DELETE, "/delete", lambda x: mt.DELETE),
        (mt.GET, "/get", lambda x: mt.GET),
        (mt.HEAD, "/head", lambda x: mt.HEAD),
        (mt.OPTIONS, "/options", lambda x: mt.OPTIONS),
        (mt.PATCH, "/patch", lambda x: mt.PATCH),
        (mt.POST, "/post", lambda x: mt.POST),
        (mt.PUT, "/put", lambda x: mt.PUT),
        (mt.TRACE, "/trace", lambda x: mt.TRACE),
    ],
)
def test_route_methods(method, pattern, handler):
    router = Router()
    http_method = getattr(router, method.lower())
    http_method(pattern, handler)

    route = router.get_handlers()[(method, pattern)]
    assert isinstance(route, Route)
    assert route.pattern == pattern
    assert route.method == method
    assert route.handler(5) == method


def test_route_handle():
    method, pattern, handler = (mt.ANY, "/any", lambda x: mt.ANY)
    router = Router()

    router.handle(pattern, handler)

    route = router.get_handlers()[(method, pattern)]
    assert isinstance(route, Route)
    assert route.pattern == pattern
    assert route.method == method
    assert route.handler(5) == method


def test_route_mount():
    router = Router()

    router.get("/hello", lambda x: x)

    router2 = Router()
    router2.get("/sub-hello", lambda x: x)

    router.mount("/sub/", router2)

    route = router.get_handlers()[(mt.GET, "/sub/sub-hello")]
    assert isinstance(route, Route)
    assert route.pattern == "/sub/sub-hello"
    assert route.method == mt.GET
    assert route.handler(5) == 5


def test_duplicate_route():
    router = Router()

    router.get("/hello", lambda x: x)
    router.get("/hello/world", lambda x: x)

    with pytest.raises(TypeError):
        router.get("/hello", lambda x: x)

    router2 = Router()
    router2.get("world", lambda x: x)
    with pytest.raises(TypeError):
        router.mount("/hello/", router2)


def test_route_use_middleware():
    router = Router().use(lambda x: x).use(lambda x: x * 2)

    router.get("/hello", lambda x: x)
    assert len(router._handlers[(mt.GET, "/hello")].middlewares) == 2


def test_route_inline_middleware():
    router = Router().use(lambda x: x).use(lambda x: x * 2)

    router.include(lambda x: x * 3).get("/hello", lambda x: x)
    assert len(router.get_handlers()[(mt.GET, "/hello")].middlewares) == 3
    assert not router._inline_middlewares


def test_make_router():
    router = Router().use(lambda x: x).use(lambda x: x * 2)
    new_router = router.make_router()
    assert len(new_router._middlewares) == 0
    assert len(new_router._handlers) == 0
