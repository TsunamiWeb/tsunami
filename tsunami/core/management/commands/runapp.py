from tsunami import web
from tsunami.core.management.base import BaseCommand, CommandError
from tsunami.core import make_app
from aiohttp import GunicornUVLoopWebWorker
from gunicorn.six import iteritems
import asyncio
import uvloop
import os
import logging
import gunicorn.app.base


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class TsunamiGunicornApplication(gunicorn.app.base.BaseApplication):

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(TsunamiGunicornApplication, self).__init__()

    def load_config(self):
        config = dict([(key, value) for key, value in iteritems(self.options)
                       if key in self.cfg.settings and value is not None])
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


class Command(BaseCommand):

    def check(self):
        if not os.path.exists('.tsunami'):
            raise CommandError('Invalid tsunami project')

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            'name', metavar='name',
            help='Name of app',
        )
        parser.add_argument(
            '--port', '-P', metavar='port',
            default=8000,
            help='Listen port',
        )

        parser.add_argument(
            '--logging', '-L', metavar='port',
            default='INFO',
            help='Logging Level',
        )

        parser.add_argument(
            '--address', '-H', metavar='address',
            default='127.0.0.1',
            help='Listen address',
        )

        parser.add_argument(
            '--mode', '-M', metavar='mode',
            default='default',
            choices=['default', 'gunicorn'],
            help='Run directly or by gunicorn',
        )

        parser.add_argument(
            '--gunicorn-args', '-G', metavar='argA:valA;argB:valB',
            help=(
                'gunicorn arguments, '
                'only available on mode `gunicorn`')
        )

    def execute(self, **options):
        _appname = options.get('name')
        _address = options.get('address')
        _port = options.get('port')
        _logging = options.get('logging')
        _mode = options.get('mode')
        _gargs = options.get('gunicorn_args')

        logging.info(f'Server started, listen on {_address}:{_port}')
        app = make_app(_appname)
        if _mode == 'default':
            web.run_app(app, port=_port)
        elif _mode == 'gunicorn':
            _gconf = {
                'worker_class': 'aiohttp.GunicornUVLoopWebWorker',
                'bind': f'{_address}:{_port}'
            }
            if _gargs:
                _gconf.update(
                    dict([kv.split(':') for kv in _gargs.split(';')]))

            TsunamiGunicornApplication(
                app,
                _gconf
            ).run()
