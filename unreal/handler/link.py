# *_* coding=utf8 *_*
#!/usr/bin/env python

from unreal.utils import ipv4
from unreal.handler import base

class Link(base.BaseHandler):

    def get(self, uuid):
        url = self.db.get("SELECT * FROM url WHERE uuid=%s", uuid)
        remote_ip_v4 = ipv4.to_int(self.request.remote_ip)
        if url is not None:
            ori_url = url['url']
            self.db.execute("UPDATE url SET pv=pv+1 WHERE id=%s", url['id'])
            self.db.execute("INSERT INTO pv_log(url_id, remote_ip_v4) VALUES(%s, %s)", url['id'], remote_ip_v4)

            redirect_url = ori_url if ori_url.startswith('http://') else 'http://%s' % ori_url
            self.redirect(redirect_url)
        else:
            self.redirect("/")
