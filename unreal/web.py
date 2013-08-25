#*_* coding=utf8 *_*
#!/usr/bin/env python

import os

from unreal import config
from unreal import handler
from unreal import greentornado

import tornado
from tornado import web

from tornado import httpserver

CONF = config.CONF


class Application(web.Application):

    def __init__(self):
        application_settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "template"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=CONF.debug)

        web.Application.__init__(self, **application_settings)


def greenify_handlers(handlers):
    g_handlers = list()
    for (route_name, hanlder_cls) in handlers:
        g_handler = greentornado.greenify(hanlder_cls)
        g_handlers.append((route_name, g_handler))

    return g_handlers


def create_application():
    # Statement our handlers.
    proxy_handlers = [(r"/", handler.proxy.RootProxy),
                      (r".*", handler.proxy.ProxyHandler)]
    proxy_handlers = greenify_handlers(proxy_handlers)

    main_handlers = [(r"/", handler.main.Index)]
    main_handlers = greenify_handlers(main_handlers)

    # Create our application that handle multiple host.
    application = Application()
    application.add_handlers(CONF.main_site_host, main_handlers)
    application.add_handlers(".*", proxy_handlers)

    return application


def start():
    app = create_application()
    sockets = tornado.netutil.bind_sockets(CONF.http_listen_port)
    server = httpserver.HTTPServer(app)
    server.add_sockets(sockets)
    greentornado.Hub.start()
