
import os

from unreal import http
from unreal import greentornado

from tornado import web
from tornado import httpserver


class ProxyHandler(web.RequestHandler):

    def proxy_get(self):
        http_connection = http.HTTPConnection(self.request.host)
        http_connection.request(
            "GET", self.request.uri, headers=self.request.headers)
        response = http_connection.getresponse()
        return response

    def get(self):
        excluded_headers = ["transfer-encoding"]
        response = self.proxy_get()
        response_status, response_headers = response.status, response.getheaders()
        response_body = response.read()

        for key, value in response_headers:
            if key.lower() not in excluded_headers:
                self.set_header(key, value)

        self.set_status(response_status)
        if response_status in [200]:
            self.finish(response_body)

class RootProxy(ProxyHandler):
    pass


class Application(web.Application):

    def __init__(self):
        handlers = [(r"/", RootProxy),
                    (r".*", ProxyHandler)]

        g_handlers = self.greenify_handlers(handlers)

        application_settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "template"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=True)

        web.Application.__init__(self, g_handlers, **application_settings)

    def greenify_handlers(self, handlers):
        g_handlers = list()
        for (route_name, hanlder_cls) in handlers:
            g_handler = greentornado.greenify(hanlder_cls)
            g_handlers.append((route_name, g_handler))

        return g_handlers


def start():
    http_server = httpserver.HTTPServer(Application(), xheaders=True)
    http_server.listen(80)
    greentornado.Hub.start()
