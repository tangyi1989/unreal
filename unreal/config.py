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
    ("main_site_host", "www.gg654.com"),
    ("admin_site_host", "admin.gg654.com"),
    ("session_expire_seconds", 3600),
    ("mysql_host", "127.0.0.1"),
    ("mysql_user", "root"),
    ("mysql_pasword", "tang"),
    ("mysql_db", "unreal"),
]


class Config(object):

    def __init__(self):
        self.data = dict(config)

    def __getattr__(self, key):
        return self.data.get(key)

CONF = Config()
