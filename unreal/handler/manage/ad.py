# *_* coding=utf8 *_*
#!/usr/bin/env python

from unreal import enum
from unreal import config
from unreal import exception
from unreal.utils import ipv4
from unreal.utils import shortuuid
from unreal.handler import base
from unreal.handler.base import require_login, require_admin

CONF = config.CONF


class AdList(base.BaseHandler):

    @require_login
    def get(self):
        user_id = self.user['id']
        ad_list = self.db.query("SELECT *, sf_ad.id AS ad_id "
                                "FROM sf_ad JOIN url ON sf_ad.url_id=url.id "
                                "WHERE sf_ad.owner_id=%s AND sf_ad.status=%s", user_id, enum.AdStatus.Active)
        self.render("manage/ad/list.html", ad_list=ad_list)


class SingleAdHandler(base.BaseHandler):

    def get_own_ad(self, ad_id):
        ad_record = self.db.get("SELECT *, sf_ad.id AS ad_id, url.id AS url_id "
                                "FROM sf_ad JOIN url ON sf_ad.url_id=url.id "
                                "WHERE sf_ad.id=%s AND sf_ad.status=%s", ad_id, enum.AdStatus.Active)

        if ad_record is None:
            raise exception.PromptRedirect("不存在的记录")

        if self.user['id'] != ad_record['owner_id'] and not self.is_admin:
            raise exception.PromptRedirect("您无权查看此记录")

        return ad_record


class AdDetail(SingleAdHandler):

    @require_login
    def get(self, ad_id):
        ad_record = self.get_own_ad(int(ad_id))
        return self.render("manage/ad/detail.html", ad_record=ad_record)


class AdAdd(SingleAdHandler):

    @require_login
    def get(self):
        return self.render("manage/ad/add.html")


class AdModify(SingleAdHandler):

    @require_login
    def get(self, ad_id):
        ad_record = self.get_own_ad(int(ad_id))
        return self.render("manage/ad/modify.html", ad_record=ad_record)


class AdPVLog(SingleAdHandler):

    @require_login
    def get(self, ad_id):
        ad_record = self.get_own_ad(ad_id)

        logs = self.db.query(
            "SELECT * FROM pv_log WHERE url_id=%s "
            "ORDER BY 1 DESC LIMIT 10", ad_record['id'])

        map(lambda log: log.setdefault(
            'ip_address', ipv4.to_address(log['remote_ip_v4'])), logs)

        self.render("manage/ad/pv_log.html", ad_record=ad_record, logs=logs)


class AdAction(SingleAdHandler):

    @require_login
    def get(self):
        method = self.get_argument("method")
        if method == "delete":
            self.delete()
        else:
            raise exception.PromptRedirect("错误的参数")

    @require_login
    def post(self):
        method = self.get_argument("method")
        if method == "add":
            self.add()
        elif method == "modify":
            self.modify()
        else:
            raise exception.PromptRedirect("错误的参数")

    def modify(self):
        ad_id = int(self.get_argument('ad_id'))
        name = self.get_argument('name')
        server_ip = self.get_argument('server_ip')
        link = self.get_argument('link')
        comment = self.get_argument('comment')
        kf_qq = self.get_argument("kf_qq")
        url = self.get_argument("url")

        ad_record = self.get_own_ad(ad_id)
        self.db.execute(
            "UPDATE sf_ad SET name=%s, server_ip=%s, link=%s, comment=%s, kf_qq=%s WHERE id=%s",
            name, server_ip, link, comment, kf_qq, ad_id)
        self.db.execute(
            "UPDATE url SET url=%s WHERE id=%s", url, ad_record['url_id'])

        return self.prompt_and_redirect("修改成功", "/manage/advertisement/detail/%s" % ad_id)

    def delete(self):
        ad_id = int(self.get_argument('ad_id'))
        ad_record = self.get_own_ad(ad_id)
        self.db.execute("UPDATE sf_ad SET status=%s WHERE id=%s",
                        enum.AdStatus.Deleted, ad_record['ad_id'])

        return self.prompt_and_redirect("删除成功")

    def add(self):
        name = self.get_argument("name")
        server_ip = self.get_argument("server_ip")
        kf_qq = self.get_argument("kf_qq")
        link = self.get_argument("link")
        comment = self.get_argument("comment")
        avalid_days = int(self.get_argument("avalid_days", 1))
        url = self.get_argument("url")

        uuid = shortuuid.uuid()
        url_id = self.db.execute_lastrowid(
            "INSERT INTO url(url, uuid, pv, create_time) VALUES(%s, %s, %s, NOW())",
            url, uuid, 0)

        self.db.execute("INSERT INTO sf_ad(name, url_id, comment, kf_qq, link, "
                        "server_ip, owner_id, status, expire_time, create_time) "
                        "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, "
                        "ADDDATE(NOW(), INTERVAL %s DAY), NOW())",
                        name, url_id, comment, kf_qq, link, server_ip, self.user['id'],
                        enum.AdStatus.Active, avalid_days)

        self.prompt_and_redirect("添加成功", "/manage/advertisement")
