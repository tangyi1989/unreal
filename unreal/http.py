#*_* coding=utf8 *_*
#!/usr/bin/env python

import eventlet
from eventlet.green import socket

from unreal import dns

httplib = eventlet.import_patched('httplib')


class HTTPConnection(httplib.HTTPConnection):

    def connect(self):
        self.sock = socket.socket()
        backend_address = dns.get_backend(self.host) or self.host
        self.sock.connect((backend_address, self.port))
