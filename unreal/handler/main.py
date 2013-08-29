# *_* coding=utf8 *_*
#!/usr/bin/env python


from unreal import config
from unreal.utils import json
from unreal.handler import base

CONF = config.CONF

class Index(base.BaseHandler):

    def get(self):
        self.write("Hello, world!")


class AdListJS(base.BaseHandler):

    def get(self):
        top_ads = self.db.query("SELECT * FROM sf_ad s_a "
                                "JOIN url url ON s_a.url_id=url.id "
                                "WHERE status=0 "
                                "ORDER BY s_a.weight LIMIT 8")

        # {0:name, 1:ad_url, 2:open_date, 3:link, 4:comment, 5:kf_qq, 6:server_ip}
        ad_list = []
        for ad in top_ads:
            ad_list.append(
                [ad['name'], 'http://%s/link/%s' % (CONF.main_site_host, ad['uuid']), 
                ad['open_date'].strftime('%m月/%d日/%Y年'), ad['link'], ad['comment'],
                ad['kf_qq'], ad['server_ip']])

        json_str = json.dumps(ad_list).decode('raw-unicode-escape').encode('utf-8')

        self.set_header("Content-Type", "application/javascript")
        self.render("main/ad_list.js", ad_list=json_str)

class Link(base.BaseHandler):

    def get(self, uuid):
        """
        这里有两种选择，一种是自己做统计，然后直接402, 
        另外一种是直接跳转到一个页面， 然后让其他的分析系统给我们进行统计。
        """
        url = self.db.get("SELECT * FROM url WHERE uuid=%s", uuid)
        if url is not None:
            self.db.execute("UPDATE url SET pv=pv+1 WHERE id=%s", url['id'])
            self.redirect(url['url'])
        else:
            self.redirect("/")
