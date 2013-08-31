#*_* coding=utf8 *_*
#!/usr/bin/env python

from tornado import web
from unreal import enum
from unreal import session
from unreal import config
from unreal import exception
from unreal.utils import mysql

CONF = config.CONF

def require_login(func):
    def wrapper(handler, *args, **kwargs):
        if not handler.is_login:
            raise exception.PromptRedirect("请登录后，执行操作。", "/")

        return func(handler, *args, **kwargs)
    return wrapper

def require_admin(func):
    def wrapper(handler, *args, **kwargs):
        if not handler.is_admin:
            raise exception.PromptRedirect("没有权限进行此操作。", "/")

        return func(handler, *args, **kwargs)
    return wrapper

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

    @property
    def user(self):
        return self.session.get('user')

    @property
    def is_login(self):
        return self.session.get('user') is not None

    @property
    def is_admin(self):
        user = self.session.get('user')
        return user is not None and user.get('type') == enum.Role.Admin 

    def logout(self):
        if self.is_login:
            del self.session['user']
            self.session.save()

    def prompt_and_redirect(self, message, uri=None):
        if uri is None:
            uri = self.request.headers.get('Referer', "/")
            
        return self.render("prompt.html", message=message, redirect_url=uri)

    def _handle_request_exception(self, e):
        e_type = type(e)
        referer = self.request.headers.get('Referer', "/")

        if e_type is exception.PromptRedirect:
            self.prompt_and_redirect(e.msg, e.uri or referer)
        else:
            super(BaseHandler, self)._handle_request_exception(e)
