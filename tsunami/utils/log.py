from gunicorn.glogging import Logger
import logging
import logging.config


class LogLevelSpecifyFilter(logging.Filter):

    def __init__(self, level):
        self.level = level

    def filter(self, record):

        if record.levelno == self.level:
            return True


DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'detailed': {
            'class': 'logging.Formatter',
            'format': ('[%(asctime)s, %(name)s] {%(filename)s:%(lineno)d}'
                       ' %(levelname)s - %(message)s')
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'detailed'
        }
    },
    'loggers': {

    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console'],
    },
}

def configure_logging(config_dict):

    logging.config.dictConfig(config_dict)
