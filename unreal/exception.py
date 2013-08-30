#*_* coding=utf8 *_*
#!/usr/bin/env python


# 内部的异常
class InvalidEnum(Exception):
    code = 1003
    message = "Deny access"

# 用于内部传播的异常
class UnrealException(Exception):
    """ 异常基类 """
    message = "An unknown exception occurred."
    code = 1000

    def __init__(self, message=None, **kwargs):
        self.kwargs = kwargs

        if 'code' not in self.kwargs:
            try:
                self.kwargs['code'] = self.code
            except AttributeError:
                pass

        if not message:
            try:
                message = self.message % kwargs
            except Exception:
                message = self.message

        super(UnrealException, self).__init__(message)

class LoopRequestException(UnrealException):
    code = 1001
    message = "Not allow loop request self."

class PromptRedirect(UnrealException):
    code = 1002
    message = "Display msg on error msg and redirect to uri"

    def __init__(self, msg, uri=None):
        self.msg = msg
        self.uri = uri

class DenyAccess(UnrealException):
    code = 1003
    message = "Deny access"

        