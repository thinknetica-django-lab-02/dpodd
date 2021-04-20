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
    'apps.profiles',
    ]

# for django-debug-toolbar
if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']

    INTERNAL_IPS = ['127.0.0.1']

    MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE

    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TEMPLATE_CONTEXT": True,
    }

MEDIA_ROOT = 'media/'
MEDIA_URL = '/media/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
    ]

CKEDITOR_UPLOAD_PATH = "uploads/"

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': env('client_id'),
            'secret': env('secret'),
            'key': ''
        }
    }
}

REDIS_HOST = '0.0.0.0'
REDIS_PORT = '6379'

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:" + REDIS_PORT + "/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}


CELERY_BROKER_URL = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_RESULT_BACKEND = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
