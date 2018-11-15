from tsunami.core.decorators.api import standard_api
from tsunami.core.decorators.routes import route
from tsunami.conf import settings
from apps.{appname}.handlers import BaseHandler


@route('/example', pattern=settings.DEFAULT_URL_PATTERN)
class ExampleHandler(BaseHandler):

    __VERSION__ = 'v1.0'

    @standard_api
    async def get(self, request):

        return {{
            'data': 'example'
        }}

