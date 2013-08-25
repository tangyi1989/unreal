#*_* coding=utf8 *_*
#!/usr/bin/env python

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