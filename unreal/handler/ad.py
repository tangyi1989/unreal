# *_* coding=utf8 *_*
#!/usr/bin/env python


from unreal import enum
from unreal import config
from unreal.utils import json
from unreal.handler import base

CONF = config.CONF


class AdListJS(base.BaseHandler):

    def get(self):
        top_ads = self.db.query("SELECT * FROM sf_ad s_a "
                                "JOIN url url ON s_a.url_id=url.id "
                                "WHERE status=%s "
                                "ORDER BY 1 DESC LIMIT 8", enum.AdStatus.Active)

        # {0:name, 1:ad_url, 2:open_date, 3:link, 4:comment, 5:kf_qq, 6:server_ip}
        ad_list = []
        for ad in top_ads:
            ad_list.append(
                [ad['name'], 'http://%s/link/%s' % (CONF.site_host, ad['uuid']),
                 None, ad['link'], ad['comment'], ad['kf_qq'], ad['server_ip']])

        json_str = json.dumps(ad_list).decode(
            'raw-unicode-escape').encode('utf-8')

        self.set_header("Content-Type", "application/javascript")
        self.render("javascript/global_ad.js", ad_list=json_str)
