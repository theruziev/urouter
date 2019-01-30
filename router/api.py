import logging
from collections import defaultdict
from typing import Dict, Callable, List

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
        self._handlers: Dict[tuple, Route] = defaultdict(
            lambda: defaultdict(dict)
        )  # pragma: no cover
        self._inline_middlewares = []

    def use(self, middleware: Callable):
        self._middlewares.append(middleware)
        return self

    def handle(self, pattern: str, handler: Callable):
        self.method(mt.ANY.value, pattern, handler)

    def _get_inline_middlewares(self):
        middlewares = self._inline_middlewares
        self._inline_middlewares = []
        return middlewares

    def mount(self, pattern: str, router: "Router"):
        handlers = router.get_handlers()
        pattern = pattern[:-1] if pattern.endswith("/") else pattern
        for route in handlers.values():
            route_pattern = route.pattern[1:] if route.pattern.startswith("/") else route.pattern
            self.method(
                route.method, f"{pattern}/{route_pattern}", route.handler, route.middlewares
            )

    def include(self, inline_middleware: List[Callable]) -> "Router":
        self._inline_middlewares.append(inline_middleware)
        return self

    def method(self, method: str, pattern: str, handler: Callable, middlewares=None):
        middlewares = middlewares or []
        all_middlewares = self._middlewares + self._get_inline_middlewares() + middlewares

        if (method, pattern) not in self._handlers:
            self._handlers[(method, pattern)] = Route(method, pattern, handler, all_middlewares)
            return
        raise TypeError("Duplicate pattern and method")

    def connect(self, pattern: str, handler: Callable):
        self.method(mt.CONNECT.value, pattern, handler)

    def delete(self, pattern: str, handler: Callable):
        self.method(mt.DELETE.value, pattern, handler)

    def get(self, pattern: str, handler: Callable):
        self.method(mt.GET.value, pattern, handler)

    def head(self, pattern: str, handler: Callable):
        self.method(mt.HEAD.value, pattern, handler)

    def options(self, pattern: str, handler: Callable):
        self.method(mt.OPTIONS.value, pattern, handler)

    def patch(self, pattern: str, handler: Callable):
        self.method(mt.PATCH.value, pattern, handler)

    def post(self, pattern: str, handler: Callable):
        self.method(mt.POST.value, pattern, handler)

    def put(self, pattern: str, handler: Callable):
        self.method(mt.PUT.value, pattern, handler)

    def trace(self, pattern: str, handler: Callable):
        self.method(mt.TRACE.value, pattern, handler)

    def get_handlers(self) -> Dict[tuple, Route]:
        return self._handlers

    def make_router(self):
        return Router()

    def export(self):
        pass  # pragma: no cover
