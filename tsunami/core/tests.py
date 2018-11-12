from tornado.testing import AsyncHTTPTestCase
from tornado.platform.asyncio import AsyncIOMainLoop
from os.path import dirname
from uvtor.conf import settings
from uvtor.core import make_app

import sys
import os


class BaseTestCase(AsyncHTTPTestCase):

    def get_app(self):
        name = dirname(sys.modules[self.__module__].__file__).split('/')[-1]
        try:
            sys.path.index(os.path.join(settings.ROOT_DIR, 'apps', name))
        except ValueError:
            sys.path.insert(1, os.path.join(settings.ROOT_DIR, 'apps', name))
        return make_app(name, False)

    def get_new_ioloop(self):
        return AsyncIOMainLoop()
