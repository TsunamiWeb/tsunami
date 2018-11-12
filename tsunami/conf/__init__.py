import os
import sys


class Settings(object):

    def __init__(self):
        sys.path.insert(0, os.getcwd())
        settings = __import__('settings')
        for _ in dir(settings):
            if not (_.startswith('__') and _.endswith('__')):
                setattr(self, _, getattr(settings, _))

try:
    settings = Settings()
except ModuleNotFoundError:
    settings = None


__ALL__ = [
    settings
]
