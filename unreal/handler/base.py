#*_* coding=utf8 *_*
#!/usr/bin/env python

from tornado import web
from unreal import session
from unreal import config

CONF = config.CONF


class BaseHandler(web.RequestHandler):

    @property
    def session(self):
        if hasattr(self, '_session'):
            return self._session
        else:
            sessionid = self.get_secure_cookie('sid')
            expire_seconds = CONF.session_expire_seconds

            self._session = session.RedisSession(
                self.application.session_store,
                sessionid, expires_days=expire_seconds)

        return self._session
