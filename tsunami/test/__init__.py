from tsunami import test_utils
from tsunami import web
from tsunami.utils import get_appname
from tsunami.core import make_app


class BaseTestCase(test_utils.AioHTTPTestCase):

    async def get_application(self):

        appname = get_appname(self.__class__)
        app = make_app(appname)
        return app
