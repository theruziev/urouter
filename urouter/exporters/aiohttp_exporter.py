# Reference: https://github.com/rob-blackbourn/aiohttp-route-middleware
import logging
from functools import partial
from typing import Callable
from urouter.constants import Method as mt
from urouter.api import Router
from aiohttp import web


logger = logging.getLogger(__name__)


class AioHttpRouter(Router):
    def __init__(self, app: web.Application):
        super(AioHttpRouter, self).__init__()
        self.app = app

    @classmethod
    def _prepare_middleware(cls, middlewares):
        for middleware in middlewares:
            if getattr(middleware, "__middleware_version__", None) == 1:
                yield middleware, True
            else:
                logger.warning('old-style middleware "{!r}" deprecated'.format(middleware))
                yield middleware, False

    @classmethod
    def _make_middleware_handler(cls, middleware, handler):
        async def invoke(request):
            return await middleware(request, handler)

        return invoke

    @classmethod
    def _make_handler(cls, handler, middlewares):
        for middleware, new_style in cls._prepare_middleware(reversed(middlewares)):
            if new_style:
                handler = partial(middleware, handler=handler)
            else:
                handler = cls._make_middleware_handler(middleware, handler)
        return handler

    def export(self):
        handlers = self.get_handlers()
        for route in handlers.values():
            handler = self._make_handler(route.handler, route.middlewares)
            self.app.router.add_route(route.method, route.pattern, handler, name=route.name)

    def handle(self, pattern: str, handler: Callable):
        self.method("*", pattern, handler)

    def method(self, method: str, pattern: str, handler: Callable, middlewares=None, name=None):
        if method in [mt.HEAD.value, mt.TRACE.value, mt.CONNECT.value]:
            raise NotImplementedError(f"Method: {method} not implemented.")
        super().method(method, pattern, handler, middlewares, name)

    def make_router(self):
        return AioHttpRouter(self.app)
