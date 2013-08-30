#*_* coding=utf8 *_*
#!/usr/bin/env python

import os
import re
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
            cookie_secret="secret",
            debug=CONF.debug)

        web.Application.__init__(self, **application_settings)

    def _get_host_handlers(self, request):
        # Modified: Just match one handler one time.
        host = request.host.lower().split(':')[0]
        matches = []
        for pattern, handlers in self.handlers:
            if pattern.match(host):
                matches.extend(handlers)
                break

        # Look for default host if not behind load balancer (for debugging)
        if not matches and "X-Real-Ip" not in request.headers:
            for pattern, handlers in self.handlers:
                if pattern.match(self.default_host):
                    matches.extend(handlers)
                    break

        return matches or None

    def _insert_default_handlers(self, handlers):
        if self.settings.get("static_path"):
            settings = self.settings
            path = self.settings["static_path"]
            handlers = list(handlers or [])
            static_url_prefix = settings.get("static_url_prefix",
                                             "/static/")
            static_handler_class = settings.get("static_handler_class",
                                                web.StaticFileHandler)
            static_handler_args = settings.get("static_handler_args", {})
            static_handler_args['path'] = path
            for pattern in [re.escape(static_url_prefix) + r"(.*)",
                            r"/(favicon\.ico)", r"/(robots\.txt)"]:
                handlers.insert(0, (pattern, static_handler_class,
                                    static_handler_args))

            return handlers


def greenify_handlers(handlers):
    g_handlers = list()
    for (route_name, hanlder_cls) in handlers:
        g_handler = greentornado.greenify(hanlder_cls)
        g_handlers.append((route_name, g_handler))

    return g_handlers


def create_application():
    application = Application()

    # Statement our handlers.
    proxy_handlers = [(r"/", handler.proxy.RootProxy),
                      (r"/js/global_ad.js", handler.ad.AdListJS),
                      (r".*", handler.proxy.ProxyHandler)]
    proxy_handlers = greenify_handlers(proxy_handlers)
    proxy_handlers = application._insert_default_handlers(proxy_handlers)

    handlers = [(r"/", handler.index.Index),
                (r"/login", handler.index.Login),
                (r"/logout", handler.index.Logout),
                (r"/manage|manage/advertisment", handler.manage.Advertisement),
                (r"/link/(\w+)", handler.link.Link)]
    handlers = greenify_handlers(handlers)
    handlers = application._insert_default_handlers(handlers)

    # Create our application that handle multiple host.
    application.add_handlers(CONF.site_host, handlers)
    application.add_handlers(".*", proxy_handlers)

    return application


def start():
    app = create_application()
    sockets = tornado.netutil.bind_sockets(CONF.http_listen_port)
    server = httpserver.HTTPServer(app)
    server.add_sockets(sockets)
    greentornado.Hub.start()
