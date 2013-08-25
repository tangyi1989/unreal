#*_* coding=utf8 *_*
#!/usr/bin/env python

import os

from unreal import handler
from unreal import config
from unreal import greentornado

from tornado import web
from tornado import httpserver

CONF = config.CONF

class Application(web.Application):

    def __init__(self):
        handlers = [(r"/", handler.proxy.RootProxy),
                    (r".*", handler.proxy.ProxyHandler)]

        g_handlers = self.greenify_handlers(handlers)

        application_settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "template"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=CONF.debug)

        web.Application.__init__(self, g_handlers, **application_settings)

    def greenify_handlers(self, handlers):
        g_handlers = list()
        for (route_name, hanlder_cls) in handlers:
            g_handler = greentornado.greenify(hanlder_cls)
            g_handlers.append((route_name, g_handler))

        return g_handlers


def start():
    http_server = httpserver.HTTPServer(Application(), xheaders=True)
    http_server.listen(CONF.http_listen_port)
    greentornado.Hub.start()
