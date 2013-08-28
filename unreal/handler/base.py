#*_* coding=utf8 *_*
#!/usr/bin/env python

from tornado import web
from unreal import session
from unreal import config
from unreal.utils import mysql

CONF = config.CONF


class BaseHandler(web.RequestHandler):

    @property
    def session(self):
        if not hasattr(self, '_session'):
            sessionid = self.get_secure_cookie('sid')
            expire_seconds = CONF.session_expire_seconds

            self._session = session.RedisSession(
                self.application.session_store,
                sessionid, expire_seconds=expire_seconds)

            if not sessionid:
                    self.set_secure_cookie('sid', self._session.id,
                                           expires_days=None)

        return self._session

    @property
    def db(self):
        return mysql.Connection(CONF.mysql_host, CONF.mysql_db,
                                CONF.mysql_user, CONF.mysql_pasword)
