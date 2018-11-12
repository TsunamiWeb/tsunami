from tsunami.core.management.base import BaseCommand, CommandError
import os
import shutil
import re
import tsunami


class Command(BaseCommand):

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            'name', metavar='name',
            help='Name of app',
        )

    def check(self):
        if not os.path.exists('.tsunami'):
            raise CommandError('Invalid tsunami project')

    def _is_valid_name(self, name):
        if not re.match(r'^[a-zA-Z]+[\w_]+$', name):
            raise CommandError('Invalid project name')

    def _init_handler(self, _appname):
        for dir_name, subdir_list, file_list in os.walk(
                os.path.join('apps', _appname)):
            for _file in file_list:
                if not _file.endswith('.tpl'):
                    continue
                _path = os.path.join(dir_name, _file[:-4])
                shutil.move(
                    os.path.join(dir_name, _file),
                    _path,
                    )
                if _file == 'main.py.tpl':
                    with open(_path) as _f:
                        _handler = _f.read()
                    _handler = _handler.format(
                        appname=_appname
                        )
                    with open(_path, 'w') as _f:
                        _f.write(_handler)

    def _init_test(self, _appname):
        _appname_upper = ''.join(
            [_p.capitalize() for _p in _appname.split('_')])
        for dir_name, subdir_list, file_list in os.walk(
                os.path.join('tests', _appname)):
            for _file in file_list:
                if not _file.endswith('.tpl'):
                    continue
                _path = os.path.join(dir_name, _file[:-4])
                shutil.move(
                    os.path.join(dir_name, _file),
                    _path,
                    )
                if _file == 'v0.py.tpl':
                    with open(_path) as _f:
                        _test = _f.read()
                    _test = _test.format(
                        appname_upper=_appname_upper
                        )
                    with open(_path, 'w') as _f:
                        _f.write(_test)

    def _init_routes(self, _appname):
        _path = os.path.join(
            'apps',
            _appname, 'routes', 'v0', '__init__.py')
        for dir_name, subdir_list, file_list in os.walk(
                os.path.join('apps', _appname, 'routes')):
            for _file in file_list:
                if not _file.endswith('.tpl'):
                    continue
                _path = os.path.join(dir_name, _file[:-4])
                shutil.move(
                    os.path.join(dir_name, _file),
                    _path,
                    )
        with open(_path) as _f:
            _routes = _f.read()
            _routes = _routes.format(
                appname=_appname
                )
        with open(_path, 'w') as _f:
            _f.write(_routes)

    def execute(self, **options):
        _appname = options.get('name')
        self._is_valid_name(_appname)
        _template_dir = os.path.join(
            tsunami.__path__[0], '_templates', 'app_template')
        _test_template_dir = os.path.join(
            tsunami.__path__[0], '_templates', 'test_template')

        shutil.copytree(_template_dir, os.path.join('apps', _appname))
        # shutil.copytree(_test_template_dir, os.path.join('tests', _appname))

        self._init_handler(_appname)
        # self._init_test(_appname)

        print(f'Successfully create app {_appname}')
