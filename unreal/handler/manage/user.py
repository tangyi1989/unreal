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

class ChangePassword(base.BaseHandler):
    
    @require_login
    def get(self):
        return self.render("manage/user/change_password.html")

class UserAdd(base.BaseHandler):
    
    @require_admin
    def get(self):
        return self.render("manage/user/add.html")

class UserList(base.BaseHandler):
    
    @require_admin
    def get(self):
        user_list = self.db.query("SELECT * FROM user")
        return self.render("manage/user/list.html", user_list=user_list)

class UserAction(base.BaseHandler):
    
    def post(self):
        method = self.get_argument("method")
        if method == "change_password":
            self.change_password()
        elif method == "add":
            self.add_user()
        else:
            raise exception.PromptRedirect("不支持的方法")

    def get(self):
        pass

    @require_login
    def change_password(self):
        old_password = self.get_argument("old_password")
        new_password = self.get_argument("new_password")
        user = self.db.get("SELECT * FROM user WHERE id=%s", self.user['id'])
        if user['password'] != old_password:
            raise PromptRedirect("原始密码错误，请重新输入")

        self.db.execute("UPDATE user SET password=%s WHERE id=%s", new_password, user['id'])
        self.logout()

        self.prompt_and_redirect("密码修改成功，请重新登陆", "/")

    @require_admin
    def add_user(self):
        username = self.get_argument("username")
        password = self.get_argument("password")

        user_count = self.db.get("SELECT COUNT(0) AS count FROM user WHERE name=%s", username)['count']
        if user_count > 0:
            raise exception.PromptRedirect("用户名已存在")

        self.db.execute("INSERT INTO user(name, password, status, `limit`, type, create_time) VALUES(%s, %s, %s, %s, %s, NOW())",
            username, password, enum.UserStatus.Active, 0, enum.Role.Normal)

        self.prompt_and_redirect("添加用户成功")

    @require_admin
    def delete_user(self):
        pass
        