# *_* coding=utf8 *_*
#!/usr/bin/env python

from unreal.handler import base

class Index(base.BaseHandler):
    def get(self):
        self.write("Hello, world!")