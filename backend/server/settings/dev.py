from server.settings.base import *

# Development Config

SECRET_KEY = 'django-insecure-g&3=ceur3j^^z!wu^%j+e4v(n$oy9ui4%o1l1ik24ihs2%7&_@'

DEBUG = True


ALLOWED_HOSTS = ["*"]

INSTALLED_APPS.append(
    "debug_toolbar",
)

# The Debug Toolbar is mostly implemented in a middleware
# The order of MIDDLEWARE is important
MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware",)


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


CORS_ALLOW_ALL_ORIGINS = True

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]


CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
]


INTERNAL_IPS = [

    "127.0.0.1",
]
