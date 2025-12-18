import logging
import os
from pathlib import Path

import dj_database_url
import sentry_sdk
from django.core.management.utils import get_random_secret_key
from dotenv import load_dotenv
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

# Load environment variables from .env unless explicitly skipped
BASE_DIR = Path(__file__).resolve().parent.parent
if os.getenv('DJANGO_SKIP_DOTENV', '').lower() not in {'1', 'true', 'yes'}:
    load_dotenv(BASE_DIR / '.env')


# Utility helpers -----------------------------------------------------------
def get_list_from_env(var_name, default):
    """Split comma separated env vars into a clean list."""
    raw_value = os.getenv(var_name)
    if raw_value is None or not raw_value.strip():
        return default
    return [item.strip() for item in raw_value.split(',') if item.strip()]


def env_bool(var_name, default=False):
    raw_value = os.getenv(var_name)
    if raw_value is None:
        return default
    return raw_value.lower() in {'1', 'true', 'yes', 'on'}


def env_float(var_name, default=0.0):
    raw_value = os.getenv(var_name)
    if raw_value is None:
        return default
    try:
        return float(raw_value)
    except ValueError:
        return default


# Local/development defaults ------------------------------------------------
DEBUG = env_bool('DJANGO_DEBUG', True)
RUNNING_TESTS = env_bool('DJANGO_TEST', False) or os.getenv('PYTEST_CURRENT_TEST') is not None
raw_secret_key = os.getenv('DJANGO_SECRET_KEY')
if not raw_secret_key:
    if not DEBUG:
        raise RuntimeError('DJANGO_SECRET_KEY must be set when DEBUG is False.')
    raw_secret_key = get_random_secret_key()
SECRET_KEY = raw_secret_key

APP_VERSION = os.getenv('APP_VERSION', 'dev')
APP_COMMIT_SHA = os.getenv('APP_COMMIT_SHA', 'dev')
ALLOWED_HOSTS = get_list_from_env(
    'DJANGO_ALLOWED_HOSTS', ['localhost', '127.0.0.1']
)
# Always allow local healthcheck/loopback hosts even when DJANGO_ALLOWED_HOSTS is set
_local_hosts = {'localhost', '127.0.0.1'}
ALLOWED_HOSTS = list(dict.fromkeys(list(ALLOWED_HOSTS) + list(_local_hosts)))


LOG_LEVEL = os.getenv('DJANGO_LOG_LEVEL', 'DEBUG')

# Application definition ----------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'core',
    'inventory',
    'miyanBeresht',
    'miyanMadi',
    'miyanGroup',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database ------------------------------------------------------------------
DB_CONN_MAX_AGE = int(os.getenv('DB_CONN_MAX_AGE', '0'))
DATABASE_URL = os.getenv('DATABASE_URL')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
# Detect running in Docker: either explicit env var or presence of /.dockerenv
IN_DOCKER = env_bool('DJANGO_IN_DOCKER', False) or Path('/.dockerenv').exists()

# Allow overriding POSTGRES_HOST via env var; otherwise default to 'db'
# when running in Docker (compose) else 'localhost' for local dev.
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
if not POSTGRES_HOST:
    POSTGRES_HOST = 'db' if IN_DOCKER else 'localhost'

if RUNNING_TESTS:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'test_db.sqlite3',
        }
    }
elif DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=DB_CONN_MAX_AGE,
            ssl_require=env_bool('DB_SSL_REQUIRE', False),
        )
    }
elif POSTGRES_DB or POSTGRES_USER or POSTGRES_PASSWORD:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': POSTGRES_DB or 'miyan_db',
            'USER': POSTGRES_USER or 'miyan_user',
            'PASSWORD': POSTGRES_PASSWORD or 'miyan_password',
            'HOST': POSTGRES_HOST,
            'PORT': POSTGRES_PORT,
            'CONN_MAX_AGE': DB_CONN_MAX_AGE,
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# When running inside Docker allow the common service hostnames so internal
# requests from other containers (for example the telegram-bot calling
# http://backend:8000) are accepted by Django's host header check.
if IN_DOCKER:
    _docker_hosts = ['backend', 'frontend', 'telegrambot', 'telegram-bot', 'db']
    ALLOWED_HOSTS = list(dict.fromkeys(ALLOWED_HOSTS + _docker_hosts))

# Password validation -------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization ------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static & media ------------------------------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Allow overriding MEDIA_ROOT via env var to support containers where the default
# path isn't writable (e.g., host-mounted dirs with restrictive permissions).
MEDIA_URL = '/media/'
MEDIA_ROOT = os.getenv('DJANGO_MEDIA_ROOT', os.path.join(BASE_DIR, 'media'))

STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage'
        if not DEBUG
        else 'django.contrib.staticfiles.storage.StaticFilesStorage',
    },
}

# Default primary key field type --------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django REST Framework -----------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 25,
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': os.getenv('DRF_ANON_THROTTLE_RATE', '100/hour'),
        'user': os.getenv('DRF_USER_THROTTLE_RATE', '1000/hour'),
    },
}

# CORS settings -------------------------------------------------------------
CORS_ALLOWED_ORIGINS = get_list_from_env(
    'DJANGO_CORS_ALLOWED_ORIGINS',
    [
        'http://localhost:3000',
        'http://127.0.0.1:3000',
        'https://miyangroup.com',
        'https://www.miyangroup.com',
    ],
)

CORS_ALLOW_CREDENTIALS = True

# CSRF settings -------------------------------------------------------------
CSRF_TRUSTED_ORIGINS = get_list_from_env(
    'DJANGO_CSRF_TRUSTED_ORIGINS',
    [
        'http://localhost:3000',
        'http://127.0.0.1:3000',
        'https://miyangroup.com',
        'https://www.miyangroup.com',
    ],
)

# Security settings ---------------------------------------------------------
SECURE_SSL_REDIRECT = env_bool('DJANGO_SECURE_SSL_REDIRECT', not DEBUG)
SESSION_COOKIE_SECURE = env_bool('DJANGO_SESSION_COOKIE_SECURE', not DEBUG)
CSRF_COOKIE_SECURE = env_bool('DJANGO_CSRF_COOKIE_SECURE', not DEBUG)
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_NAME = os.getenv('DJANGO_CSRF_COOKIE_NAME', 'miyan_csrftoken')
CSRF_COOKIE_SAMESITE = 'None' if CSRF_COOKIE_SECURE else 'Lax'
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_NAME = os.getenv('DJANGO_SESSION_COOKIE_NAME', 'miyan_sessionid')
SESSION_COOKIE_SAMESITE = 'None' if SESSION_COOKIE_SECURE else 'Lax'
SECURE_HSTS_SECONDS = int(
    os.getenv('DJANGO_SECURE_HSTS_SECONDS', '31536000' if not DEBUG else '0')
)
SECURE_HSTS_INCLUDE_SUBDOMAINS = env_bool(
    'DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS', not DEBUG
)
SECURE_HSTS_PRELOAD = env_bool('DJANGO_SECURE_HSTS_PRELOAD', not DEBUG)

# Determine whether to trust reverse proxy headers. Default to True when
# running inside Docker behind a host nginx (IN_DOCKER), otherwise respect
# explicit env var or fall back to not DEBUG.
if os.getenv('DJANGO_TRUST_PROXY_HEADERS') is None:
    TRUST_PROXY_HEADERS = bool(IN_DOCKER or (not DEBUG))
else:
    TRUST_PROXY_HEADERS = env_bool('DJANGO_TRUST_PROXY_HEADERS', not DEBUG)

USE_X_FORWARDED_HOST = env_bool('DJANGO_USE_X_FORWARDED_HOST', TRUST_PROXY_HEADERS)
SECURE_PROXY_SSL_HEADER = (
    ('HTTP_X_FORWARDED_PROTO', 'https') if TRUST_PROXY_HEADERS else None
)

if not SECURE_SSL_REDIRECT:
    SECURE_HSTS_SECONDS = 0

# Additional security settings ----------------------------------------------
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin'
SECURE_CROSS_ORIGIN_EMBEDDER_POLICY = 'require-corp'
SECURE_CROSS_ORIGIN_RESOURCE_POLICY = 'same-origin'
X_FRAME_OPTIONS = 'DENY'

# Session settings ----------------------------------------------------------
SESSION_COOKIE_AGE = 1209600  # 2 weeks in seconds
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# Authentication ------------------------------------------------------------
LOGIN_URL = '/admin/login/'
LOGIN_REDIRECT_URL = '/admin/'
LOGOUT_REDIRECT_URL = '/admin/login/'

# Observability / error tracking --------------------------------------------
SENTRY_DSN = os.getenv('SENTRY_DSN')
SENTRY_ENVIRONMENT = os.getenv('SENTRY_ENVIRONMENT', 'development')
SENTRY_TRACES_SAMPLE_RATE = env_float('SENTRY_TRACES_SAMPLE_RATE', 0.0)
SENTRY_PROFILES_SAMPLE_RATE = env_float('SENTRY_PROFILES_SAMPLE_RATE', 0.0)

if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        environment=SENTRY_ENVIRONMENT,
        release=APP_VERSION,
        integrations=[
            DjangoIntegration(),
            LoggingIntegration(level=logging.INFO, event_level=logging.ERROR),
        ],
        traces_sample_rate=SENTRY_TRACES_SAMPLE_RATE,
        profiles_sample_rate=SENTRY_PROFILES_SAMPLE_RATE,
        send_default_pii=True,
    )

# Logging -------------------------------------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'fmt': '%(asctime)s %(levelname)s %(name)s %(message)s %(pathname)s %(lineno)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'json',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': LOG_LEVEL,
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': LOG_LEVEL,
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}

# Shared secret used by the telegram bot to request tokens securely
BOT_SHARED_SECRET = os.getenv('TELEGRAM_SHARED_SECRET', '')
