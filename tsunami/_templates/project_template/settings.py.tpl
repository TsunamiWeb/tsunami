from os.path import abspath, dirname
from os import environ


DEBUG = environ.get('DEBUG') != 'False'

LISTEN_PORT = 8000

COOKIE_SECRET = {cookie_secret}

ROOT_DIR = dirname(abspath(__file__))

DEFAULT_URL_PATTERN = '/api/{{version}}/{{appname}}/{{path}}'

# Add your settings here.
