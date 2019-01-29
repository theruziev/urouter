import pytest

from router import Router, Route
from router.constants import Method as mt


@pytest.mark.parametrize(
    "method, pattern, handler",
    [
        (mt.CONNECT, "/connect", lambda x: mt.CONNECT.value),
        (mt.DELETE, "/delete", lambda x: mt.DELETE.value),
        (mt.GET, "/get", lambda x: mt.GET.value),
        (mt.HEAD, "/head", lambda x: mt.HEAD.value),
        (mt.OPTIONS, "/options", lambda x: mt.OPTIONS.value),
        (mt.PATCH, "/patch", lambda x: mt.PATCH.value),
        (mt.POST, "/post", lambda x: mt.POST.value),
        (mt.PUT, "/put", lambda x: mt.PUT.value),
        (mt.TRACE, "/trace", lambda x: mt.TRACE.value),
    ],
)
def test_route_methods(method, pattern, handler):
    r = Router()
    http_method = getattr(r, method.value.lower())
    http_method(pattern, handler)

    route = r.get_handlers()[(method.value, pattern)]
    assert isinstance(route, Route)
    assert route.pattern == pattern
    assert route.method == method.value
    assert route.handler(5) == method.value


def test_route_handle():
    method, pattern, handler = (mt.ANY, "/any", lambda x: mt.ANY.value)
    r = Router()

    r.handle(pattern, handler)

    route = r.get_handlers()[(method.value, pattern)]
    assert isinstance(route, Route)
    assert route.pattern == pattern
    assert route.method == method.value
    assert route.handler(5) == method.value


def test_route_mount():
    r = Router()

    r.get("/hello", lambda x: x)

    r2 = Router()
    r2.get("/sub-hello", lambda x: x)

    r.mount("/sub/", r2)

    route = r.get_handlers()[(mt.GET.value, "/sub/sub-hello")]
    assert isinstance(route, Route)
    assert route.pattern == "/sub/sub-hello"
    assert route.method == mt.GET.value
    assert route.handler(5) == 5


def test_duplicate_route():
    r = Router()

    r.get("/hello", lambda x: x)
    r.get("/hello/world", lambda x: x)

    with pytest.raises(TypeError):
        r.get("/hello", lambda x: x)

    r2 = Router()
    r2.get("world", lambda x: x)
    with pytest.raises(TypeError):
        r.mount("/hello/", r2)


def test_route_use_middleware():
    r = Router().use(lambda x: x).use(lambda x: x * 2)

    r.get("/hello", lambda x: x)
    assert len(r._handlers[(mt.GET.value, "/hello")].middlewares) == 2


def test_route_inline_middleware():
    r = Router().use(lambda x: x).use(lambda x: x * 2)

    r.include(lambda x: x * 3).get("/hello", lambda x: x)
    assert len(r.get_handlers()[(mt.GET.value, "/hello")].middlewares) == 3
    assert not r._inline_middlewares


def test_make_router():
    router = Router().use(lambda x: x).use(lambda x: x * 2)
    new_router = router.make_router()
    assert len(new_router._middlewares) == 0
    assert len(new_router._handlers) == 0
