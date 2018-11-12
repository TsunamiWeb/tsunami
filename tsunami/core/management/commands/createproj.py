from tsunami.core.management.base import BaseCommand, CommandError
import os
import shutil
import re
import tsunami
import base64
import uuid


class Command(BaseCommand):

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            'name', metavar='name',
            help='Name of project',
        )

    def _is_valid_name(self, name):
        if not re.match(r'^[a-zA-Z]+[\w_-]+$', name):
            raise CommandError('Invalid project name')

    def _init_settings(self, path):
        with open(path) as _f:
            _settings = _f.read()
        _settings = _settings.format(
            cookie_secret="'{}'".format(base64.b64encode(
                uuid.uuid4().bytes + uuid.uuid4().bytes).decode())
            )

        with open(path, 'w') as _f:
            _f.write(_settings)

    def execute(self, **options):
        _projname = options.get('name')
        self._is_valid_name(_projname)
        _template_dir = os.path.join(
            tsunami.__path__[0], '_templates', 'project_template')

        shutil.copytree(_template_dir, _projname)

        for dir_name, subdir_list, file_list in os.walk(_projname):
            for _file in file_list:
                if not _file.endswith('.tpl'):
                    continue
                shutil.move(
                    os.path.join(dir_name, _file),
                    os.path.join(dir_name, _file[:-4]),
                    )
                if _file == 'settings.py.tpl':
                    self._init_settings(
                        os.path.join(dir_name, _file[:-4]))
        print(f'Successfully create project {_projname}')
