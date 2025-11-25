import os
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

# Load environment variables from .env
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

# Utility helpers -----------------------------------------------------------
def get_list_from_env(var_name, default):
    """Split comma separated env vars into a clean list."""
    raw_value = os.getenv(var_name)
    if raw_value is None:
        return default
    return [item.strip() for item in raw_value.split(',') if item.strip()]


def env_bool(var_name, default=False):
    raw_value = os.getenv(var_name)
    if raw_value is None:
        return default
    return raw_value.lower() in {'1', 'true', 'yes', 'on'}


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'insecure-default-key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env_bool('DJANGO_DEBUG', False)
ALLOWED_HOSTS = get_list_from_env(
    'DJANGO_ALLOWED_HOSTS',
    ['localhost', '127.0.0.1', 'miyangroup.com', '.miyangroup.com'],
)

LOG_LEVEL = os.getenv('DJANGO_LOG_LEVEL', 'INFO')

# Application definition
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

# Database
DB_CONN_MAX_AGE = int(os.getenv('DB_CONN_MAX_AGE', '60'))
DATABASE_URL = os.getenv('DATABASE_URL')

default_db_config = {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': os.getenv('POSTGRES_DB', 'miyan_db'),
    'USER': os.getenv('POSTGRES_USER', 'miyan_user'),
    'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'miyan_password'),
    'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
    'PORT': os.getenv('POSTGRES_PORT', '5432'),
    'CONN_MAX_AGE': DB_CONN_MAX_AGE,
}

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=DB_CONN_MAX_AGE,
            ssl_require=env_bool('DB_SSL_REQUIRE', False),
        )
    }
else:
    DATABASES = {'default': default_db_config}

# Password validation
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

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

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

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django REST Framework
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
}

# CORS settings
CORS_ALLOWED_ORIGINS = get_list_from_env(
    'DJANGO_CORS_ALLOWED_ORIGINS',
    [
        'https://miyangroup.com',
        'https://www.miyangroup.com',
        'https://app.miyangroup.com',
        'http://localhost:3000',
        'http://127.0.0.1:3000',
    ],
)

CORS_ALLOW_CREDENTIALS = True

# CSRF settings
CSRF_TRUSTED_ORIGINS = get_list_from_env(
    'DJANGO_CSRF_TRUSTED_ORIGINS',
    [
        'https://miyangroup.com',
        'https://www.miyangroup.com',
        'https://app.miyangroup.com',
        'https://api.miyangroup.com',
        'http://localhost:3000',
        'http://127.0.0.1:3000',
    ],
)

# Security settings
SECURE_SSL_REDIRECT = env_bool('DJANGO_SECURE_SSL_REDIRECT', not DEBUG)
SESSION_COOKIE_SECURE = env_bool('DJANGO_SESSION_COOKIE_SECURE', not DEBUG)
CSRF_COOKIE_SECURE = env_bool('DJANGO_CSRF_COOKIE_SECURE', not DEBUG)
CSRF_COOKIE_SAMESITE = 'None' if CSRF_COOKIE_SECURE else 'Lax'
SESSION_COOKIE_SAMESITE = 'None' if SESSION_COOKIE_SECURE else 'Lax'
SECURE_HSTS_SECONDS = int(os.getenv('DJANGO_SECURE_HSTS_SECONDS', '31536000' if not DEBUG else '0'))
SECURE_HSTS_INCLUDE_SUBDOMAINS = env_bool('DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS', not DEBUG)
SECURE_HSTS_PRELOAD = env_bool('DJANGO_SECURE_HSTS_PRELOAD', not DEBUG)
TRUST_PROXY_HEADERS = env_bool('DJANGO_TRUST_PROXY_HEADERS', not DEBUG)
USE_X_FORWARDED_HOST = env_bool('DJANGO_USE_X_FORWARDED_HOST', TRUST_PROXY_HEADERS)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https') if TRUST_PROXY_HEADERS else None

if not SECURE_SSL_REDIRECT:
    SECURE_HSTS_SECONDS = 0

# Additional security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Session settings
SESSION_COOKIE_AGE = 1209600  # 2 weeks in seconds
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# Authentication
LOGIN_URL = '/admin/login/'
LOGIN_REDIRECT_URL = '/admin/'
LOGOUT_REDIRECT_URL = '/admin/login/'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
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
    },
}
