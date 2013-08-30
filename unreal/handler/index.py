# *_* coding=utf8 *_*
#!/usr/bin/env python

from unreal import config
from unreal import exception
from unreal.handler import base

CONF = config.CONF


class Index(base.BaseHandler):

    def get(self):
        ad_list = self.db.query("SELECT * FROM sf_ad s_a "
                                "JOIN url url ON s_a.url_id=url.id AND status=0")

        map(lambda row: row.setdefault('site_url', 'http://%s/link/%s' %
            (CONF.site_host, row['uuid'])), ad_list)

        return self.render("index.html", ad_list=ad_list)


class Login(base.BaseHandler):

    def post(self):
        username = self.get_argument("username")
        password = self.get_argument("password")
        user = self.db.get("SELECT * FROM user WHERE name=%s AND status=%s",
                           username, 0)
        if user is None or user["password"] != password:
            raise exception.PromptRedirect("帐号或密码错误")

        self.session['user'] = user
        self.session.save()
        self.redirect("/manage")


class Logout(base.BaseHandler):

    def get(self):
        if self.is_login:
            del self.session['user']
            self.session.save()

        self.redirect("/")
