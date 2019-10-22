import logging
from collections import defaultdict
from typing import Dict, Callable, List, Union

from .constants import Method as mt

logger = logging.getLogger(__name__)


class Route:
    handler = None
    method = None
    middlewares = None
    pattern = None
    name = None

    def __init__(self, method, pattern, handler, *, middlewares=None, name=None):
        self.handler = handler
        self.method = method
        self.pattern = pattern
        self.middlewares = middlewares or []
        self.name = name


class Router:
    _handlers = None
    _middlewares = None
    _inline_middlewares = None

    def __init__(self):
        self._middlewares = []
        self._handlers: Dict[tuple, Route] = defaultdict(
            lambda: defaultdict(dict)
        )  # pragma: no cover
        self._inline_middlewares = []

    @property
    def middlewares(self):
        return self._middlewares

    def use(self, middleware: Callable):
        self._middlewares.append(middleware)
        return self

    def handle(self, pattern: str, handler: Callable):
        self.method(mt.ANY, pattern, handler)

    def _get_inline_middlewares(self):
        middlewares = self._inline_middlewares
        self._inline_middlewares = []
        return middlewares

    def mount(self, pattern: str, router: Union["Router", Callable[[], "Router"]]):
        handlers = router.get_handlers() if isinstance(router, Router) else router().get_handlers()
        pattern = pattern[:-1] if pattern.endswith("/") else pattern
        for route in handlers.values():
            route_pattern = route.pattern[1:] if route.pattern.startswith("/") else route.pattern
            self.method(
                route.method, f"{pattern}/{route_pattern}", route.handler, route.middlewares
            )

    def include(self, inline_middleware: List[Callable]) -> "Router":
        self._inline_middlewares.append(inline_middleware)
        return self

    def method(self, method: str, pattern: str, handler: Callable, middlewares=None, name=None):
        middlewares = middlewares or []
        all_middlewares = self._middlewares + self._get_inline_middlewares() + middlewares

        if (method, pattern) not in self._handlers:
            self._handlers[(method, pattern)] = Route(
                method, pattern, handler, middlewares=all_middlewares, name=name
            )
            return
        raise TypeError("Duplicate pattern and method")

    def connect(self, pattern: str, handler: Callable, name: str = None):
        self.method(mt.CONNECT, pattern, handler, name=name)

    def delete(self, pattern: str, handler: Callable, name: str = None):
        self.method(mt.DELETE, pattern, handler, name=name)

    def get(self, pattern: str, handler: Callable, name: str = None):
        self.method(mt.GET, pattern, handler, name=name)

    def head(self, pattern: str, handler: Callable, name: str = None):
        self.method(mt.HEAD, pattern, handler, name=name)

    def options(self, pattern: str, handler: Callable, name: str = None):
        self.method(mt.OPTIONS, pattern, handler, name=name)

    def patch(self, pattern: str, handler: Callable, name: str = None):
        self.method(mt.PATCH, pattern, handler, name=name)

    def post(self, pattern: str, handler: Callable, name: str = None):
        self.method(mt.POST, pattern, handler, name=name)

    def put(self, pattern: str, handler: Callable, name: str = None):
        self.method(mt.PUT, pattern, handler, name=name)

    def trace(self, pattern: str, handler: Callable, name: str = None):
        self.method(mt.TRACE, pattern, handler, name=name)

    def get_handlers(self) -> Dict[tuple, Route]:
        return self._handlers

    def make_router(self):
        return Router()

    def export(self):
        pass  # pragma: no cover
