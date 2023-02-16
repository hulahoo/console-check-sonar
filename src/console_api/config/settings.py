"""Settings for the project"""

import os

from pathlib import Path
from environs import Env

env = Env()
env.read_env("./.env")

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-8&pnw5q%u_ht#1zdz@j4n1tvw!kbcvk_3lnw6+ulo$07p998xf'

DEBUG = env("DEBUG")

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'drf_yasg',
    'django_filters',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',

    # Custom apps
    "console_api.feed.apps.FeedConfig",
    "console_api.indicator.apps.IndicatorConfig",
    "console_api.source.apps.SourceConfig",
    "console_api.tag.apps.TagConfig",
    "console_api.users.apps.UsersConfig",
    "console_api.statistics.apps.StatisticsConfig",
    "console_api.detections.apps.DetectionsConfig",
    "console_api.audit_logs.apps.AuditLogsConfig",
    "console_api.search.apps.SearchConfig",
    "console_api.platform_settings.apps.PlatformSettingsConfig",
    "console_api.context_sources.apps.ContextSourcesConfig",
    "console_api.files.apps.FilesConfig",
]

DJANGO_MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'console_api.middleware.profiling.time_profiling',

]

THIRD_PARTY_MIDDLEWARE = []
if DEBUG:
    THIRD_PARTY_MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')

MIDDLEWARE = THIRD_PARTY_MIDDLEWARE + DJANGO_MIDDLEWARE

ROOT_URLCONF = 'console_api.config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'console_api.config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        "NAME": env("APP_POSTGRESQL_NAME"),
        "USER": env("APP_POSTGRESQL_USER"),
        "PASSWORD": env("APP_POSTGRESQL_PASSWORD"),
        "HOST": env("APP_POSTGRESQL_HOST"),
        "PORT": env("APP_POSTGRESQL_PORT"),
    }
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = "/media/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.User"

CORS_ALLOWED_ORIGINS = ['*']

# DRF

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 25,
}

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

FEEDS_IMPORTING_SERVICE_URL = env(
    "FEEDS_IMPORTING_SERVICE_URL",
    "https://develop.tip-feeds-import-worker.rshb.axept.com",
)
SCORE_SERVICE_URL = env(
    "SCORE_SERVICE_URL",
    "https://data-processing-worker.develop.cti.rshb.axept.com"
)
