from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

try:
    from .local import *
except ImportError:
    pass
