from tsunami.conf import settings
from tsunami.core.handlers import BaseHandler
from tsunami.utils import log
from tsunami import web
import pkgutil
import importlib
import inspect
import logging
import os


__METHODS = ["get", "post", "delete", "put", "head", "connect", "options", "trace"]


def get_appname(cls):
    _cpath = inspect.getfile(cls)
    _common_prefix = os.path.commonprefix([_cpath, settings.ROOT_DIR])
    return os.path.relpath(_cpath, _common_prefix)[5:].split("/")[0]


def list_appnames():
    return [
        f
        for f in os.listdir(os.path.join(settings.ROOT_DIR, "apps"))
        if not f.startswith("_")
    ]


def make_app(appname, mode, *args, **kwargs):

    if mode == "gunicorn":

        async def app():
            if hasattr(settings, "LOGGING"):

                log.configure_logging(settings.LOGGING)
            elif hasattr(settings, "configure_logging"):
                log.configure_logging(settings.configure_logging())
            else:
                log.configure_logging(log.DEFAULT_LOGGING)
            app = web.Application()
            [
                auto_discover(appname, app)
                for appname in (list_appnames() if appname == "all" else [appname])
            ]
            return app

        return app
    else:
        if hasattr(settings, "LOGGING"):

            log.configure_logging(settings.LOGGING)
        elif hasattr(settings, "configure_logging"):
            log.configure_logging(settings.configure_logging())
        else:
            log.configure_logging(log.DEFAULT_LOGGING)
        app = web.Application()
        [
            auto_discover(appname, app)
            for appname in (list_appnames() if appname == "all" else [appname])
        ]
        return app


def get_routes_by_cls(cls):
    if getattr(cls, "__routes__", False):
        _c = cls()
        routes_ = []
        logging.debug(f"Add routes ({cls.__url__}, {cls})")
        for _m in __METHODS:
            routes_.append(web.route(_m, _c.__url__, getattr(_c, _m)))
        return routes_
    return []


def auto_discover(appname, app):
    handlers = importlib.import_module("apps.{}.handlers".format(appname))

    for loader, modname, ispkg in pkgutil.walk_packages(handlers.__path__):
        _module = loader.find_module(modname).load_module(modname)

        [
            app.add_routes(get_routes_by_cls(cls))
            for name, cls in inspect.getmembers(_module)
            if inspect.isclass(cls) and issubclass(cls, BaseHandler)
        ]
