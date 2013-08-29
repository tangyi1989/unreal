#*_* coding=utf8 *_*
#!/usr/bin/env python

import gzip
import cStringIO

from unreal import config
from unreal import exception
from unreal.utils import cache
from unreal.utils import html
from unreal.utils import http
from unreal.handler import base

CONF = config.CONF


class ProxyHandler(base.BaseHandler):

    def prevent_loop_request_self(self):
        # To prevent loop request self
        if self.request.headers.get("DangerTag") == "unreal":
            raise exception.LoopRequestException()

    def proxy_request(self, ungzip=False, without_cache=False):
        self.prevent_loop_request_self()

        cache_key = cache.CacheKey(
            "REQUEST", self.request.host, self.request.method, self.request.uri)

        if not without_cache:
            result = cache.get(cache_key)
            if result is not None:
                return result

        http_connection = http.HTTPConnection(self.request.host)
        headers = self.request.headers.copy()

        # Set a danger tag for prevent future loop request.
        headers["DangerTag"] = "unreal"
        http_connection.request(
            self.request.method, self.request.uri, headers=headers)
        response = http_connection.getresponse()

        response_headers = [(k.lower(), v) for k, v in response.getheaders()]
        response_headers_dict = dict(response_headers)
        content_encoding = response_headers_dict.get('content-encoding')

        # HTTP Connection would not ungzip http content for us.
        # So we decompress it by our self.
        if content_encoding == 'gzip' and ungzip:
            compressed_stream = cStringIO.StringIO(response.read())
            data = gzip.GzipFile(fileobj=compressed_stream).read()
            response_headers_dict.pop('content-encoding')
        else:
            data = response.read()

        result = response.status, response_headers_dict.items(), data
        if response.status == 200:
            cache.set(
                cache_key, result, expire_seconds=CONF.backend_expire_seconds)

        return result

    def proxy(self):

        status, headers, body = self.proxy_request()
        expect_headers = ['set-cookie', 'content-encoding']
        
        for key, value in headers:
            if key.lower() in expect_headers:
                self.set_header(key, value)

            if key.lower() == 'content-type':
                self.set_header('Content-Type', value)

        self.set_status(status)
        if status in [200]:
            self.write(body)
            self.finish()

    def get(self):
        return self.proxy()


class RootProxy(ProxyHandler):
    
    def get(self):
        cache_key = cache.CacheKey(
            "MAIN_PAGE", self.request.host, self.request.method, self.request.uri)

        cached_response = cache.get(cache_key)
        if cached_response is not None:
            status, headers, modified_body = cached_response
        else:
            status, headers, body = self.proxy_request(ungzip=True)
            html_headers = [
                '<script type="text/javascript" src="/js/ad_list.js"></script>',
                '<script type="text/javascript" src="/static/js/jquery.js"></script>',
                '<script type="text/javascript" src="/static/js/ad_framework/main.js"></script>']

            body = html.convert_encoding(body)
            modified_body = html.add_html_header(body, html_headers)
            cache_response = (status, headers, modified_body)
            cache.set(cache_key, cache_response, CONF.backend_expire_seconds)
        

        expect_headers = ["set-cookie"]
        for key, value in headers:
            if key.lower() in expect_headers:
                self.set_header(key, value)

        self.set_status(status)
        if status in [200]:
            self.write(modified_body)
            self.finish()
