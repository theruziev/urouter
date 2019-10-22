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
        return StarletteRouter(self.app)

    def handle(self, pattern: str, handler: Callable):
        raise TypeError("Method required for Starlette")

    def export(self):
        for route in self.get_handlers().values():
            r = Route(route.pattern, route.handler, methods=[route.method], name=route.name)
            for m in route.middlewares:
                if inspect.isclass(m):
                    r.app = m(r.app)
                else:
                    m.app = r.app
                    r.app = m
            self.app.router.routes.append(r)
