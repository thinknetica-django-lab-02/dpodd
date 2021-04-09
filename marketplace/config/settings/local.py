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

# SOCIALACCOUNT_PROVIDERS = {
#     'google': {
#         # For each OAuth based provider, either add a ``SocialApp``
#         # (``socialaccount`` app) containing the required client
#         # credentials, or list them here:
#         'APP': {
#             'client_id': '123',
#             'secret': '456',
#             'key': ''
#         }
#     }
# }
