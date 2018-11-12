from tsunami import web
from functools import wraps




def route(path, pattern=None):

    def decorator(cls):
        _path = path
        version = getattr(cls, '__VERSION__', 'v1.0')
        if pattern:
            _path = pattern.format(
                path=path,
                appname=__APPNAME__,
                version=version)
        _path = _path.replace('//', '/')
        cls.__routes__ = True
        cls.__url__ = _path
        cls.__appname__ = __APPNAME__
        return cls

    return decorator
