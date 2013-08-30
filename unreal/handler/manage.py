# *_* coding=utf8 *_*
#!/usr/bin/env python

from unreal import config
from unreal import exception
from unreal.utils import shortuuid
from unreal.handler import base
from unreal.handler.base import require_login, require_admin

CONF = config.CONF


class Advertisement(base.BaseHandler):

    @require_login
    def get(self):
        user_id = self.user['id']
        ad_list = self.db.query("SELECT * FROM sf_ad JOIN url "
                                "ON sf_ad.url_id=url.id "
                                "WHERE sf_ad.owner_id=%s", user_id)
        self.render("manage/ad.html", ad_list=ad_list)


class AdAction(base.BaseHandler):

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
