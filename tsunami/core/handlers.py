from tsunami.conf import settings
from tsunami.core.cache import cache
from tsunami import web
import functools
import pickle


class BaseHandler:

    async def get(self, request):
        raise web.HTTPMethodNotAllowed('get', '*')

    async def post(self, request):
        raise web.HTTPMethodNotAllowed('post', '*')

    async def delete(self, request):
        raise web.HTTPMethodNotAllowed('delete', '*')

    async def put(self, request):
        raise web.HTTPMethodNotAllowed('put', '*')

    async def head(self, request):
        raise web.HTTPMethodNotAllowed('head', '*')

    async def options(self, request):
        raise web.HTTPMethodNotAllowed('options', '*')

    async def trace(self, request):
        raise web.HTTPMethodNotAllowed('trace', '*')

    async def connect(self, request):
        raise web.HTTPMethodNotAllowed('connect', '*')




