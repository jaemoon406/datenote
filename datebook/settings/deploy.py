from .common import *
from django.utils.log import DEFAULT_LOGGING

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('APP_DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.environ.get('DB_NAME', 'db.sqlite'),
        'USER': os.environ.get('DB_USER', ''),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', None),
        'PORT': os.environ.get('DB_PORT', None),
        "OPTIONS": {"charset": "utf8mb4"},
    }
}

LOGGING = DEFAULT_LOGGING
LOGGING['handlers']['slack'] = {
  'level': 'ERROR',
  'filters': ['require_debug_false'],
  'class': 'datebook.slack_logger.SlackLoggerHandler',
}

LOGGING['loggers']['django'] = {
  'handlers': ['console', 'slack'],
  'level': 'INFO',
}
