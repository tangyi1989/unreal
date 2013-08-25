# *_* coding=utf8 *_*
#!/usr/bin/env python

import redis
from unreal import config

try:
    import cPickle as pickle
except ImportError:
    import pickle


CONF = config.CONF


class CacheKey(object):

    def __init__(self, *args):
        self.key_list = args

    def prefix(self, key):
        key_list = (key,) + self.key_list
        return CacheKey(*key_list)

    def key(self):
        return " || ".join(map(str, self.key_list))

    def children_key(self):
        return "%s || *" % self.key()


class RedisClient(object):

    @classmethod
    def pool(cls):
        if not hasattr(cls, "__pool__"):
            setattr(cls, "__pool__", redis.ConnectionPool())
        return getattr(cls, "__pool__")

    @classmethod
    def get_connection(cls):
        pool = cls.pool()
        return redis.Redis(
            host=CONF.cache_redis_host, port=CONF.cache_redis_port,
            db=CONF.cache_redis_db, connection_pool=pool)


def set(cache_key, obj, expire_seconds=None):
    key = cache_key.key()
    value = pickle.dumps(obj)

    redis_conn = RedisClient.get_connection()
    redis_conn.set(key, value)
    if type(expire_seconds) is int:
        redis_conn.expire(key, expire_seconds)


def get(cache_key):
    redis_conn = RedisClient.get_connection()
    value = redis_conn.get(cache_key.key())

    obj = None
    if value is not None:
        obj = pickle.loads(value)

    return obj


def delete(cache_key, include_children=True):
    """
    删除缓存，让缓存及所有依赖此缓存的key过期，例如:
    when exipire yuanzuo.wallet, it would be expire
    yuanzuo.wallet and yuanzuo.wallet.*
    PARAMETERS:
        cache_key: CacheKey的实例
    """
    redis_conn = RedisClient.get_connection()
    if include_children:
        keys = redis_conn.keys(cache_key.children_key())
        keys.append(cache_key.key())
        redis_conn.delete(*keys)
    else:
        redis_conn.delete(cache_key.key())
