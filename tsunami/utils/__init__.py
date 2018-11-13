from tsunami.conf import settings
import inspect
import os


def get_appname(cls):
    _cpath = inspect.getfile(cls)
    _common_prefix = os.path.commonprefix(
        [
            _cpath,
            settings.ROOT_DIR
        ])
    return os.path.relpath(
        _cpath, _common_prefix)[5: ].split('/')[0]


def list_appnames():
    return [
        f for f in os.listdir(
            os.path.join(settings.ROOT_DIR, 'apps')
    ) if not f.startswith('_')]
