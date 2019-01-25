import logging
from collections import defaultdict
from typing import Dict, List, Callable
from .constants import Method as mt

logger = logging.getLogger(__name__)


class Route:
    handler = None
    method = None
    middlewares = None
    pattern = None

    def __init__(self, method, pattern, handler, middlewares=None):
        self.handler = handler
        self.method = method
        self.pattern = pattern
        self.middlewares = middlewares or []


class Router:
    _handlers = None
    _middlewares = None
    _inline_middlewares = None

    def __init__(self):
        self._middlewares = []
        self._handlers: Dict[tuple, Route] = defaultdict(lambda: defaultdict(dict))
        self._inline_middlewares = []

    def use(self, middleware: Callable):
        self._middlewares.append(middleware)
        return self

    def handle(self, pattern: str, handler: Callable):
        self.method(mt.ANY, pattern, handler)

    def _get_inline_middlewares(self):
        middlewares = self._inline_middlewares
        self._inline_middlewares = []
        return middlewares

    def mount(self, pattern: str, router: "Router"):
        handlers = router.get_handlers()
        for route in handlers.values():
            self.method(
                route.method, f"{pattern}/{route.pattern}", route.handler, route.middlewares
            )

    def include(self, inline_middleware: List[Callable]) -> "Router":
        self._inline_middlewares.append(inline_middleware)
        return self

    def method(self, method: mt, pattern: str, handler: Callable, middlewares=None):
        middlewares = middlewares or []
        all_middlewares = self._middlewares + self._get_inline_middlewares() + middlewares

        if (method, pattern) not in self._handlers:
            self._handlers[(method, pattern)] = Route(method, pattern, handler, all_middlewares)
            return
        raise TypeError("Duplicate pattern and method")

    def connect(self, pattern: str, handler: Callable):
        self.method(mt.CONNECT, pattern, handler)

    def delete(self, pattern: str, handler: Callable):
        self.method(mt.DELETE, pattern, handler)

    def get(self, pattern: str, handler: Callable):
        self.method(mt.GET, pattern, handler)

    def head(self, pattern: str, handler: Callable):
        self.method(mt.HEAD, pattern, handler)

    def options(self, pattern: str, handler: Callable):
        self.method(mt.OPTIONS, pattern, handler)

    def patch(self, pattern: str, handler: Callable):
        self.method(mt.PATCH, pattern, handler)

    def post(self, pattern: str, handler: Callable):
        self.method(mt.POST, pattern, handler)

    def put(self, pattern: str, handler: Callable):
        self.method(mt.PUT, pattern, handler)

    def trace(self, pattern: str, handler: Callable):
        self.method(mt.TRACE, pattern, handler)

    def export(self):
        pass

    def get_handlers(self) -> Dict[tuple, Route]:
        return self._handlers
