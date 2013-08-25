# *_* coding=utf8 *_*
#!/usr/bin/env python

config = [
    ("cache_redis_host", "127.0.0.1"),
    ("cache_redis_port", 6379),
    ("cache_redis_db", 0),
    ("backend_expire_seconds", 300),
]


class Config(object):

    def __init__(self):
        self.data = dict(config)

    def __getattr__(self, key):
        return self.data.get(key)

CONF = Config()
