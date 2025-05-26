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

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=[])
CSRF_TRUSTED_ORIGINS = env.list("DJANGO_CSRF_TRUSTED_ORIGINS", default=[])

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

# # Celery
# CELERY_BROKER_URL = env("REDIS_URL")
# CELERY_RESULT_BACKEND = env("REDIS_URL")

# Django-Q configuration for production
Q_CLUSTER = {
    'name': 'budget_prod',
    'workers': 2,
    'recycle': 1000,
    'timeout': 60,
    'retry': 150,
    'max_attempts': 2,
    'compress': True,
    'save_limit': 100,
    'orm': 'default',
    'catch_up': False,
    'sync': False,  # async mode
    'poll': 20,  # verify new tasks every 20 seconds
    'bulk': 5,  # process up to 5 tasks at once
}

# Cache
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env("REDIS_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "KEY_PREFIX": "budget_prod",
    }
}

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Static file configuration for production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
