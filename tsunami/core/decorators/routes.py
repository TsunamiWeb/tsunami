from tsunami import web
from tsunami.utils import get_appname
from functools import wraps


def route(path, pattern=None):

    def decorator(cls):
        _path = path
        _appname = get_appname(cls)
        version = getattr(cls, '__VERSION__', 'v1.0')
        if pattern:
            _path = pattern.format(
                path=path,
                appname=_appname,
                version=version)
        _path = _path.replace('//', '/')
        cls.__routes__ = True
        cls.__url__ = _path
        cls.__appname__ = _appname
        return cls

    return decorator
