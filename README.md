# Tsunami --- Lightweight, but Powerful Async web framework

*Based on aiohttp*

* Install

```sh
pip install tsunamiweb
```

* Create Project

```sh
tsunami createproj <project-name>
```

* Create App

```sh
tsunami createapp <appname>
```

* Create a handler

```python
from tsunami.core.decorators.api import standard_api
from tsunami.core.decorators.routes import route
from tsunami.conf import settings
from apps.features.handlers import BaseHandler


@route('/example', pattern=settings.DEFAULT_URL_PATTERN)
class ExampleHandler(BaseHandler):

    __VERSION__ = 'v1.0'

    @standard_api
    async def get(self, request):

        return {
            'data': 'example'
        }
```

* Run your app

```sh
tsunami runapp <appname>
```

* Test your app

```sh
tsunami runtest <appname>
```

Then fetch your API with url ```http://127.0.0.1/api/v1.0/<appname>/example```
