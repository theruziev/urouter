Router
========
.. image:: https://img.shields.io/travis/com/bruziev/router.svg?style=flat-square
        :target: https://travis-ci.com/bruziev/router
.. image:: https://img.shields.io/codecov/c/github/bruziev/router.svg?style=flat-square
        :target: https://codecov.io/gh/bruziev/router



**This is POC, not for production use**

Installation
------------
TODO

Quickstart
----------

**Define handler in router**

.. code-block:: python

    from aiohttp import web
    from router.exporters.aiohttp_exporter import AioHttpRouter
    app = web.Application()

     async def handler(request):
        return web.Response(text="Hello World")

    router = AioHttpRouter(app)

    router.get("/home", handler)

    # At this point aiohttp is ready to register all routes
    router.export()


**Define global middleware for all routes**

.. code-block:: python

    from aiohttp import web
    from router.exporters.aiohttp_exporter import AioHttpRouter
    app = web.Application()

    @web.middleware
    async def info_middleware(request, handler):
        # some operation before handle request
        response = await handler(request)
        return response

     async def handler(request):
        return web.Response(text="Hello World")

    router = (AioHttpRouter(app)
                .use(info_middleware))

    # Register handler
    router.get("/home", handler)

    # At this point aiohttp is ready to register all routes
    router.export()


**Define inline middleware (run only for specific handler)**

.. code-block:: python

    from aiohttp import web
    from router.exporters.aiohttp_exporter import AioHttpRouter
    app = web.Application()

    @web.middleware
    async def info_middleware(request, handler):
        # some operation before handle request
        response = await handler(request)
        return response

     async def handler(request):
        return web.Response(text="Hello World")

    router = AioHttpRouter(app)
    
    # Middleware registered only for `/home` route
    router.include(info_middleware).get("/home", handler)

    # At this point aiohttp is ready to register all routes
    router.export()

**Define subrouter**

.. code-block:: python

    from aiohttp import web
    from router.exporters.aiohttp_exporter import AioHttpRouter
    app = web.Application()

    @web.middleware
    async def info_middleware(request, handler):
        # some operation before handle request
        response = await handler(request)
        return response

     async def handler(request):
        return web.Response(text="Hello World")

     async def sub_handler(request):
        return web.Response(text="Hello World")


    router = AioHttpRouter(app)

    router.include(info_middleware).get("/home", handler)
    
    # Create new router
    subrouter = router.make_router()
    subrouter.get("/hello", sub_handler)

    # All registered router become starts with prefix `/sub/` 
    # `/hello` becomes `/sub/hello`
    router.mount("/sub", subrouter)

    # At this point aiohttp is ready to register all routes
    router.export()
