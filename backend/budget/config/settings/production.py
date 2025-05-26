"""
Production settings.
"""

from .base import *  # noqa
from .base import env

# env.read_env(str(BASE_DIR / "config" / "env" / ".env.production"))  # noqa: F405

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", default=False)

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["budget-production-99c8.up.railway.app", "https://*.railway.app", "https://*.streamlit.app"])
CSRF_TRUSTED_ORIGINS = env.list("DJANGO_CSRF_TRUSTED_ORIGINS", default=["https://*.railway.app", "https://*.streamlit.app"])

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env("DB_NAME"),
        'USER': env("DB_USER"),
        'PASSWORD': env("DB_PASSWORD"),
        'HOST': env("DB_HOST"),
        'PORT': env("DB_PORT"),
    }
}

# Security
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 60 * 60 * 24 * 365  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# CORS settings
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=["https://budget-app.streamlit.app"])
CORS_ALLOW_CREDENTIALS = True

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env("REDIS_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {
                "retry_on_timeout": True,
                "retry_on_error": [ConnectionError, TimeoutError],
                "socket_keepalive": True,
                "socket_keepalive_options": {},
                "health_check_interval": 30,
                "max_connections": 5,  # FOARTE IMPORTANT - limită mică
            },
            "IGNORE_EXCEPTIONS": True,
        },
        "KEY_PREFIX": "budget_prod",
        "TIMEOUT": 300,
    }
}

# Celery config cu conexiuni limitate
CELERY_BROKER_URL = env("REDIS_URL")
CELERY_RESULT_BACKEND = env("REDIS_URL")

CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_BROKER_CONNECTION_RETRY = True
CELERY_RESULT_BACKEND_CONNECTION_RETRY = True

# FOARTE IMPORTANT - limitează conexiunile Celery
CELERY_REDIS_MAX_CONNECTIONS = 3
CELERY_WORKER_CONCURRENCY = 1  # doar 1 worker concurrent
CELERY_WORKER_PREFETCH_MULTIPLIER = 1

CELERY_REDIS_RETRY_ON_TIMEOUT = True
CELERY_REDIS_SOCKET_KEEPALIVE = True
CELERY_REDIS_HEALTH_CHECK_INTERVAL = 30

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Static file configuration for production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
