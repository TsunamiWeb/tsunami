from tsunami.core.management.base import BaseCommand, CommandError
from tsunami.utils import log
from tsunami.core import list_appnames
from tsunami.conf import settings
import os
import sys
import pkgutil
import unittest
import logging


class Command(BaseCommand):

    def _get_tests(self, *appnames):
        if 'all' in appnames:
            return unittest.defaultTestLoader.discover(
                'apps/', top_level_dir=settings.ROOT_DIR)
        else:
            suite = unittest.suite.TestSuite()
            for app in appnames:
                suite.addTests(
                    unittest.defaultTestLoader.discover(
                        f'apps/{app}',
                        top_level_dir=settings.ROOT_DIR))
            return suite

    def check(self):
        if not os.path.exists('.tsunami'):
            raise CommandError('Invalid tsunami project')

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            'modules', metavar='name',
            nargs='+',
            help='Name of app',
            default=['all']
        )
        parser.add_argument(
            '--logging', '-L', metavar='port',
            default='warning',
            choices=['debug', 'info', 'warning', 'error'],
            type=str.lower,
            help='Logging Level'
        )

    def execute(self, **options):
        _logging = options.get('logging')

        log.DEFAULT_LOGGING[
                'handlers']['console']['level'] = _logging.upper()

        unittest.TextTestRunner().run(
            self._get_tests(*options.get('modules')))
