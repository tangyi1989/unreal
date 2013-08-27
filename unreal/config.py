# *_* coding=utf8 *_*
#!/usr/bin/env python

config = [
    ("redis_host", "127.0.0.1"),
    ("debug", True),
    ("redis_cache_db", 0),
    ("redis_session_db", 1),
    ("redis_port", 6379),
    ("backend_expire_seconds", 300),
    ("http_listen_port", 80),
    ("main_site_host", "127.0.0.1"),
    ("session_expire_seconds", 3600),
]


class Config(object):

    def __init__(self):
        self.data = dict(config)

    def __getattr__(self, key):
        return self.data.get(key)

CONF = Config()
