from .common import *
DEBUG = True

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
ALGORITHM = os.environ.get('ALGORITHM')
SECRET_KEY = os.environ.get('SECRET_KEY')