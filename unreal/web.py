#*_* coding=utf8 *_*
#!/usr/bin/env python

import os
import redis

import tornado
from tornado import web
from tornado import httpserver

from unreal import config
from unreal import handler
from unreal import greentornado
from unreal.session import RedisSessionStore

CONF = config.CONF


class Application(web.Application):

    def __init__(self):
        redis_connection = redis.Redis(
            host=CONF.redis_host, port=CONF.redis_port, db=CONF.redis_session_db)
        self.session_store = RedisSessionStore(redis_connection)

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

    main_handlers = [(r"/", handler.main.Index),
                     (r"/link/(w+)", handler.main.Link)]
    main_handlers = greenify_handlers(main_handlers)

    # Create our application that handle multiple host.
    application = Application()
    application.add_handlers(CONF.main_site_host, main_handlers)
    # match all host except main site.
    application.add_handlers("(?!%s)" % CONF.main_site_host, proxy_handlers)

    return application


def start():
    app = create_application()
    sockets = tornado.netutil.bind_sockets(CONF.http_listen_port)
    server = httpserver.HTTPServer(app)
    server.add_sockets(sockets)
    greentornado.Hub.start()
