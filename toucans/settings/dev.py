from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'dh=tb7bn2r$bei&j@(c!ev_!fpigdl_0pm)ku31+f^(!&!sxo@'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'toucans',
        'USER': 'toucans',
        'PASSWORD': 'toucans',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

try:
    from .local import *
except ImportError:
    pass
