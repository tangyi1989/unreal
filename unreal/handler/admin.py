# *_* coding=utf8 *_*
#!/usr/bin/env python

from datetime import datetime

from unreal import exception
from unreal.utils import shortuuid
from unreal.handler import base


def require_login(func):
    def wrapper(handler, *args, **kwargs):
        if handler.session.get("user") is None:
            raise exception.PromptRedirect("请登录后，执行操作。", "/login")

        return func(handler, *args, **kwargs)
    return wrapper


class AdminBaseHandler(base.BaseHandler):

    def prompt_and_redirect(self, message, uri):
        return self.render("admin/prompt.html", message=message, redirect_url=uri)

    def _handle_request_exception(self, e):
        e_type = type(e)
        referer = self.request.headers.get('Referer', "/")

        if e_type is exception.PromptRedirect:
            self.prompt_and_redirect(e.msg, e.uri or referer)
        else:
            super(AdminBaseHandler, self)._handle_request_exception(e)


class AdList(AdminBaseHandler):

    @require_login
    def get(self):
        ad_list = self.db.query("SELECT * FROM sf_ad s_a "
                                "JOIN url url ON s_a.url_id=url.id AND status=0")
        self.render("admin/ad_list.html", ad_list=ad_list)


class AdAction(AdminBaseHandler):

    @require_login
    def post(self):
        method = self.get_argument("method")
        if method == "add":
            self.add()
        else:
            raise exception.PromptRedirect("错误的参数")

    def add(self):
        name = self.get_argument("name")
        server_ip = self.get_argument("server_ip")
        kf_qq = self.get_argument("kf_qq")
        link = self.get_argument("link")
        comment = self.get_argument("comment")
        weight = int(self.get_argument("weight"))
        avalid_days = int(self.get_argument("avalid_days", 1))
        open_date = datetime.strptime(self.get_argument("open_date"), "%Y-%m-%d")

        url = self.get_argument("url")

        uuid = shortuuid.uuid()
        url_id = self.db.execute_lastrowid(
            "INSERT INTO url(url, uuid, pv, create_time) VALUES(%s, %s, %s, NOW())",
            url, uuid, 0)

        self.db.execute("INSERT INTO sf_ad(name, url_id, open_date, comment, "
                        "kf_qq, link, server_ip, weight, status, expire_time, create_time) "
                        "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, "
                        "ADDDATE(NOW(), INTERVAL %s DAY), NOW())",
                        name, url_id, open_date, comment, kf_qq, link, server_ip, weight,
                        0, avalid_days)

        self.prompt_and_redirect("添加成功", "/")


class Login(AdminBaseHandler):

    def get(self):
        self.render("admin/login.html")

    def post(self):
        username = self.get_argument("username")
        password = self.get_argument("password")
        user = self.db.get("SELECT * FROM user WHERE name=%s AND status=%s",
                           username, 0)
        if user is None or user["password"] != password:
            raise exception.PromptRedirect("帐号或密码错误")

        self.session['user'] = user
        self.session.save()
        self.redirect("/")
