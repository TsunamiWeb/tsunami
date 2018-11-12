from tornado.test.util import unittest
from uvtor.core.management.base import BaseCommand
import os
import sys
import pkgutil


class Command(BaseCommand):

    TEST_MODULES = [
    ]

    def all(self):
        return unittest.defaultTestLoader.loadTestsFromNames(
            self.TEST_MODULES)

    def _get_tests(self, *modules):
        if len(modules) > 0:
            for _module in set(modules):
                print(_module)
                module_ = __import__(f'tests.{_module}')
                for loader, modname, ispkg in pkgutil.walk_packages(
                        module_.__path__, module_.__name__ + '.'):
                    if not ispkg:
                        self.TEST_MODULES.append(modname)
        else:
            _tests = __import__('tests')
            for loader, modname, ispkg in pkgutil.walk_packages(
                    _tests.__path__, _tests.__name__ + '.'):
                if not ispkg:
                    self.TEST_MODULES.append(modname)

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            '--modules', metavar='name',
            nargs='+',
            help='Name of app',
            default=[]
        )

    def execute(self, **options):
        sys.path.insert(0, os.getcwd())
        self._get_tests(*options.get('modules'))
        unittest.TextTestRunner().run(self.all())
