Router
========
.. image:: https://img.shields.io/travis/com/bruziev/router.svg?style=flat-square
        :target: https://travis-ci.com/bruziev/router
.. image:: https://img.shields.io/codecov/c/github/bruziev/router.svg?style=flat-square
        :target: https://codecov.io/gh/bruziev/router

This is POC, not for production use

Installation
------------
TODO

Quickstart
----------
**Default behavior registering handler in router**

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

**Global middleware**

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


**Inline middleware(Run only for specific handler)**

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

    router.include(info_middleware).get("/home", handler)

    # Registered all route in aiohttp
    router.export()

**Sub router**

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

    sub_router = router.make_router()
    sub_router.get("/hello", sub_handler)

    # All registered router become starts with `/sub/` prefix
    # `/hello` become `/sub/hello`
    router.mount("/sub", sub_router)

    # Registered all route in aiohttp
    router.export()