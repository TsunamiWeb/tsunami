from tsunami.core.management.base import BaseCommand, CommandError
import os
import shutil
import re


class Command(BaseCommand):

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            'name', metavar='name',
            help='Name of app',
        )

    def _is_valid_name(self, name):
        if not re.match(r'^[a-zA-Z]+[\w_]+$', name):
            raise CommandError('Invalid project name')

    def execute(self, **options):
        _appname = options.get('name')
        shutil.rmtree(os.path.join('apps', _appname))
        print(f'Successfully remove app {_appname}')
