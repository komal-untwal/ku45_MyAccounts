import logging
import os
import time
import datetime
from logging.config import dictConfig

import flask
from flask import request, current_app, g

# from app.logging_config.log_formatters import RequestFormatter
from rfc3339 import rfc3339

from app import config

log_con = flask.Blueprint('log_con', __name__)


# @log_con.before_app_request
# def before_request_logging():


@log_con.after_app_request
def after_request_logging(response):
    if request.path == '/favicon.ico':
        return response
    elif request.path.startswith('/static'):
        return response
    elif request.path.startswith('/bootstrap'):
        return response

    now = time.time()
    dt = datetime.datetime.fromtimestamp(now)
    timestamp = rfc3339(dt, utc=True)
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)

    log_params = [
        ('method', request.method),
        ('path', request.path),
        ('status', response.status_code),
        ('time', timestamp),
        ('ip', ip),
    ]

    request_id = request.headers.get('X-Request-ID')
    if request_id:
        log_params.append(('request_id', request_id))

    parts = []
    for name, value in log_params:
        part = name + ': ' + str(value) + ', '
        parts.append(part)
    line = " ".join(parts)
    # this triggers a log entry to be created with whatever is in the line variable

    log = logging.getLogger('request')
    log.info('This is request info log!' + line)

    return response


@log_con.before_app_first_request
def setup_logs():
    # set the name of the apps log folder to logs
    logdir = config.Config.LOG_DIR
    # make a directory if it doesn't exist
    if not os.path.exists(logdir):
        os.mkdir(logdir)
    logging.config.dictConfig(LOGGING_CONFIG)


LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },

    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # Default is stderr
        },
        'file.handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': os.path.join(config.Config.LOG_DIR, 'handler.log'),
            'maxBytes': 10000000,
            'backupCount': 5,
        },
        'file.handler.myapp': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': os.path.join(config.Config.LOG_DIR, 'myapp.log'),
            'maxBytes': 10000000,
            'backupCount': 5,
        },
        'file.handler.request': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': os.path.join(config.Config.LOG_DIR, 'request.log'),
            'maxBytes': 10000000,
            'backupCount': 5,
        },
        'file.handler.errors': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': os.path.join(config.Config.LOG_DIR, 'errors.log'),
            'maxBytes': 10000000,
            'backupCount': 5,
        },
        'file.handler.csvUploads': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': os.path.join(config.Config.LOG_DIR, 'csvUploads.log'),
            'maxBytes': 10000000,
            'backupCount': 5,
        },
        'file.handler.sqlalchemy': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': os.path.join(config.Config.LOG_DIR, 'sqlalchemy.log'),
            'maxBytes': 10000000,
            'backupCount': 5,
        },
        'file.handler.werkzeug': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': os.path.join(config.Config.LOG_DIR, 'werkzeug.log'),
            'maxBytes': 10000000,
            'backupCount': 5,
        },
        'file.handler.userBalance': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': os.path.join(config.Config.LOG_DIR, 'userBalanceUpdate.log'),
            'maxBytes': 10000000,
            'backupCount': 5,
        },
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['default', 'file.handler'],
            'level': 'DEBUG',
            'propagate': True
        },
        '__main__': {  # if __name__ == '__main__'
            'handlers': ['default', 'file.handler'],
            'level': 'DEBUG',
            'propagate': True
        },
        'werkzeug': {  # if __name__ == '__main__'
            'handlers': ['file.handler.werkzeug'],
            'level': 'DEBUG',
            'propagate': False
        },
        'sqlalchemy.engine': {  # if __name__ == '__main__'
            'handlers': ['file.handler.sqlalchemy'],
            'level': 'INFO',
            'propagate': False
        },
        'myApp': {  # if __name__ == '__main__'
            'handlers': ['file.handler.myapp'],
            'level': 'DEBUG',
            'propagate': False
        },
        'request': {  # if __name__ == '__main__'
            'handlers': ['file.handler.request'],
            'level': 'DEBUG',
            'propagate': False
        },
        'myerrors': {  # if __name__ == '__main__'
            'handlers': ['file.handler.errors'],
            'level': 'DEBUG',
            'propagate': False
        },
        'csvUploads': {  # if __name__ == '__main__'
            'handlers': ['file.handler.csvUploads'],
            'level': 'DEBUG',
            'propagate': False
        },
        'userBalance': {  # if __name__ == '__main__'
            'handlers': ['file.handler.userBalance'],
            'level': 'DEBUG',
            'propagate': False
        },

    }
}
