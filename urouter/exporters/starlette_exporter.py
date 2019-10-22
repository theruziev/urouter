import inspect
import logging
from typing import Callable

from starlette.applications import Starlette
from starlette.routing import Route

from urouter.api import Router

logger = logging.getLogger(__name__)


class StarletteRouter(Router):
    def __init__(self, app: Starlette):
        super(StarletteRouter, self).__init__()
        self.app = app

    def make_router(self):
        router = StarletteRouter(self.app)
        router._middlewares = self.middlewares.copy()
        return router

    def handle(self, pattern: str, handler: Callable):
        raise TypeError("Method required for Starlette")

    def export(self):
        for route in self.get_handlers().values():
            starlette_route = Route(
                route.pattern, route.handler, methods=[route.method], name=route.name
            )
            for middleware in route.middlewares:
                if inspect.isclass(middleware):
                    starlette_route.app = middleware(starlette_route.app)
                else:
                    middleware.app = starlette_route.app
                    starlette_route.app = middleware
            self.app.router.routes.append(starlette_route)
