from tsunami.core import response as _resp
from tsunami.core.exceptions import APIException
from tsunami import web
from functools import wraps
import traceback


def standard_api(func):

    @wraps(func)
    async def decorator(request, *args, **kwargs):
        try:
            result = await func(request, *args, **kwargs)
            if isinstance(result, dict) or not result:
                response = {'code': _resp.CODE_0_SUCCESS}
                response.update(result or {})
                return web.json_response(response)
            else:
                return result
        except (APIException, Exception) as e:
            # print(traceback.format_exc())
            if not hasattr(e, 'code'):
                print(traceback.format_exc())
                e.code = 1
            return web.json_response({'code': e.code, 'error_msg': str(e)})

    return decorator
