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

    # Registered all route in aiohttp
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

    # Registered all route in aiohttp
    router.export()


**Define inline middleware(Run only for specific handler)**

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

    # Registered all route in aiohttp
    router.export()

**Define sub router**

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
    sub_router = router.make_router()
    sub_router.get("/hello", sub_handler)

    # All registered router become starts with prefix `/sub/` 
    # `/hello` become `/sub/hello`
    router.mount("/sub", sub_router)

    # Registered all route in aiohttp
    router.export()
