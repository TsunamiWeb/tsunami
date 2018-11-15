from tsunami.conf import settings
from tsunami.core.handlers import BaseHandler
from tsunami.utils import list_appnames
from tsunami import web
import pkgutil
import importlib
import inspect


__METHODS = [
    'get', 'post', 'delete', 'put', 'head', 'connect', 'options', 'trace']


def make_app(appname, autoreload=True):
    app = web.Application()
    [
        auto_discover(
            appname, app
        ) for appname in (
            list_appnames() if appname == 'all' else [appname])
    ]
    return app


def get_routes_by_cls(cls):
    if getattr(cls, '__routes__', False):
        _c = cls()
        routes_ = []
        print(f'Add routes ({cls.__url__}, {cls})')
        for _m in __METHODS:
            routes_.append(
                web.route(_m, _c.__url__, getattr(_c, _m)))
        return routes_
    return []


def auto_discover(appname, app):
    handlers = importlib.import_module('apps.{}.handlers'.format(appname))

    for loader, modname, ispkg in pkgutil.walk_packages(handlers.__path__):
        _module = loader.find_module(modname).load_module(modname)
        [
            app.add_routes(get_routes_by_cls(cls))
                for name, cls in inspect.getmembers(_module)
                    if inspect.isclass(cls) and issubclass(cls, BaseHandler)
        ]
