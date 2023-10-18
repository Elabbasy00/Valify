from server.settings.base import *
import os

# Production Config


SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = False


ALLOWED_HOSTS = [os.environ.get("host")]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'db',
        'PORT': 5432,
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD')
    },
}


CORS_ALLOW_ALL_ORIGINS = False

CORS_ORIGIN_ALLOW_ALL = False

CORS_ALLOWED_ORIGINS = []


CSRF_TRUSTED_ORIGINS = []
