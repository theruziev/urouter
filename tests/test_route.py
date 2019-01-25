from functools import partial

from router import Router
from router.constants import Method as mt


def test_route():
    r = Router().use(lambda x: x).use(lambda x: x * 2)

    r.get("/hello", lambda x: x)
    assert len(r._handlers[(mt.GET, "/hello")].middlewares) == 2

    r.include(lambda x: x * 3).get("/hello2", lambda x: x)
    assert len(r._handlers[(mt.GET, "/hello2")].middlewares) == 3
    assert not r._inline_middlewares
