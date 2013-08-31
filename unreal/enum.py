#*_* coding=utf8 *_*
#!/usr/bin/env python

from unreal import exception

class Enum(object):
    def __init__(self, **kwargs):
        self.data = kwargs

    def __getattr__(self, key):
        value = self.data.get(key)
        if value is None:
            raise exception.InvalidEnum()

        return value

Role = Enum(Normal=0, Admin=1)
UserStatus = Enum(Active=0, Deleted=1)
AdStatus = Enum(Active=0, Deleted=1)