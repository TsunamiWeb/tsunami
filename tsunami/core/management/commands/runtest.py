from tsunami.core.management.base import BaseCommand
from tsunami.utils import list_appnames
from tsunami.conf import settings
import os
import sys
import pkgutil
import unittest


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

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            'modules', metavar='name',
            nargs='+',
            help='Name of app',
            default=['all']
        )

    def execute(self, **options):
        unittest.TextTestRunner().run(
            self._get_tests(*options.get('modules')))
