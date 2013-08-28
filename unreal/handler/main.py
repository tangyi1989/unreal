# *_* coding=utf8 *_*
#!/usr/bin/env python

from unreal.handler import base

class Index(base.BaseHandler):
    def get(self):
        self.write("Hello, world!")

class Main(base.BaseHandler):
    pass

class Login(base.BaseHandler):
    def get(self):
        self.write("Hello, world!")

class Link(base.BaseHandler):
    def get(self, url):
        """
        这里有两种选择，一种是自己做统计，然后直接402, 
        另外一种是直接跳转到一个页面， 然后让其他的分析系统给我们进行统计。
        """
        self.render("base.html")