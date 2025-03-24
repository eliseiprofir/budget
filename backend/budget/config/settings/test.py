"""
Test settings.
"""

from .base import *  # noqa
from .base import env

env.read_env(str(BASE_DIR / "config" / "env" / ".env.test"))  # noqa: F405

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "test-secret-key"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.test.sqlite3',  # noqa: F405
    }
}

# Celery
CELERY_TASK_ALWAYS_EAGER = True  # Execute tasks synchronously
CELERY_TASK_EAGER_PROPAGATES = True

# Cache
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

# Email
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Password hashers (faster for testing)
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]
