from .base import *

DEBUG = True


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

INSTALLED_APPS += [
    'apps.main',
    ]

# for django-debug-toolbar
if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']

    INTERNAL_IPS = ['127.0.0.1']

    MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE

    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TEMPLATE_CONTEXT": True,
    }