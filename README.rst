uRouter
========
.. image:: https://img.shields.io/travis/com/bruziev/urouter.svg?style=flat-square
        :target: https://travis-ci.com/bruziev/urouter
.. image:: https://img.shields.io/codecov/c/github/bruziev/urouter.svg?style=flat-square
        :target: https://codecov.io/gh/bruziev/urouter



**This is POC, not for production use**

Installation
------------

.. code-block:: bash

    pip install urouter

Quickstart
----------

**Define handler in router**

.. code-block:: python

    from aiohttp import web
    from urouter.exporters.aiohttp_exporter import AioHttpRouter
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
    from urouter.exporters.aiohttp_exporter import AioHttpRouter
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
    from urouter.exporters.aiohttp_exporter import AioHttpRouter
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
    from urouter.exporters.aiohttp_exporter import AioHttpRouter
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

**Private/Public router**

.. code-block:: python

    from aiohttp import web
    from urouter.exporters.aiohttp_exporter import AioHttpRouter
    app = web.Application()

    @web.middleware
    async def auth_middleware(request, handler):

        return web.HTTPForbidden()

    async def public(request):
        return web.Response(text="Hello World")

    async def private(request):
        return web.Response(text="Private Zone")

    router = AioHttpRouter(app)
    private_route = router.make_router().use(auth_middleware)

    # Adding public handler
    router.get("/home", public)
    
    # Adding public handler
    private_route.get("/private", private)
    
    # Mount private router to main router
    router.mount("/", private_route)

    # At this point aiohttp is ready to register all routes
    router.export()
