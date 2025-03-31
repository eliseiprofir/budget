"""
Local development settings.
"""

from .base import *  # noqa
from .base import env

env.read_env(str(BASE_DIR / "config" / "env" / ".env.local"))  # noqa: F405

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY", default="django-insecure-rvshwjb(%&j#l+y#-z2g@&gkpj5r67wo%dz9zj&3g8nrpp4k0w")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env("DB_NAME", default="budget"),
        'USER': env("DB_USER", default="postgres"),
        'PASSWORD': env("DB_PASSWORD", default="postgres"),
        'HOST': env("DB_HOST", default="db"),
        'PORT': env("DB_PORT", default="5432"),
    }
}

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8501",
    "http://127.0.0.1:8501",
]
CORS_ALLOW_CREDENTIALS = True

# Celery
CELERY_BROKER_URL = 'redis://redis:6379'
CELERY_RESULT_BACKEND = 'redis://redis:6379'

# Cache
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "KEY_PREFIX": "budget_local",
    }
}

# Email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
