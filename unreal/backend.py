#*_* coding=utf8 *_*
#!/usr/bin/env python

backend_list = [("9pk.118sh.com", "113.105.175.243")]

BACKEND_DICT = dict()
AccessList = map(lambda x:x[0], backend_list)

def get_backend(host):
    return BACKEND_DICT.get(host)


def init():
    for (host, ip) in backend_list:
        BACKEND_DICT.setdefault(host, ip)

init()
