from django.utils.translation import gettext_lazy as _

from utils.shortcuts import generate_random_string

import django_stubs_ext
from dotenv import load_dotenv
from pathlib import Path
import string
import sys
import os


django_stubs_ext.monkeypatch()
load_dotenv()


BASE_DIR: Path = Path(__file__).resolve().parent.parent

SECRET_KEY: str = os.getenv(
	'SECRET_KEY', f'django-insecure-{generate_random_string(string.ascii_letters + string.digits, 50)}'
)
DEBUG: bool = os.getenv('DEBUG', 'True') == 'True'

match sys.argv:
	case ['manage.py', 'test', *extra_options]:
		TEST = True
	case __:
		TEST = False

TELEGRAM_BOTS_HUB_PATH: str | None = os.getenv('TELEGRAM_BOTS_HUB_PATH')

CONSTRUCTOR_TELEGRAM_BOT_API_TOKEN: str | None = os.getenv('TELEGRAM_BOT_TOKEN')
CONSTRUCTOR_TELEGRAM_BOT_USERNAME: str | None = os.getenv('TELEGRAM_BOT_USERNAME')

POSTGRESQL_DATABASE_NAME: str | None = os.getenv('POSTGRESQL_DATABASE_NAME')
POSTGRESQL_DATABASE_USER: str | None = os.getenv('POSTGRESQL_DATABASE_USER')
POSTGRESQL_DATABASE_PASSWORD: str | None = os.getenv('POSTGRESQL_DATABASE_PASSWORD')


SITE_DOMAIN = 'http://127.0.0.1:8000' if DEBUG else 'https://constructor.exg1o.org'
ALLOWED_HOSTS = ['127.0.0.1', 'constructor.exg1o.org']


CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_BEAT_SCHEDULE = {
	'update_users_first_and_last_name_schedule': {
		'task': 'users.tasks.update_users_first_and_last_name',
		'schedule': 86400,  # 24 ч.
	},
	'check_confirm_code_generation_date_schedule': {
		'task': 'users.tasks.check_confirm_code_generation_date',
		'schedule': 3600,  # 1 ч.
	},
}


INSTALLED_APPS = [
	'rest_framework',
	'rest_framework.authtoken',
	'django_filters',
	'drf_standardized_errors',
	'admin_interface',
	'colorfield',
	'modeltranslation',
	'tinymce',
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'languages',
	'users',
	'telegram_bots',
	'telegram_bots.hub',
	'updates',
	'instruction',
	'donation',
	'privacy_policy',
]

REST_FRAMEWORK = {
	'EXCEPTION_HANDLER': 'drf_standardized_errors.handler.exception_handler',
}

TINYMCE_DEFAULT_CONFIG = {
	'theme': 'silver',
	'menubar': True,
	'height': 420,
	'plugins': (
		'advlist, autolink, lists, link, image, charmap,'
		'print, preview, anchor, searchreplace, visualblocks,'
		'code, fullscreen, insertdatetime, media, table, paste,'
		'help, wordcount'
	),
	'toolbar': (
		'undo redo | '
		'formatselect | '
		'bold italic backcolor | '
		'alignleft aligncenter alignright alignjustify | '
		'bullist numlist outdent indent | '
		'removeformat | '
		'help'
	),
}


MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'django.middleware.locale.LocaleMiddleware',
]


TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [
			BASE_DIR / 'constructor_telegram_bots/templates',
			BASE_DIR / 'frontend/dist',
		],
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


AUTH_USER_MODEL = 'users.User'
ROOT_URLCONF = 'constructor_telegram_bots.urls'
WSGI_APPLICATION = 'constructor_telegram_bots.wsgi.application'


DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql',
		'NAME': POSTGRESQL_DATABASE_NAME,
		'USER': POSTGRESQL_DATABASE_USER,
		'PASSWORD': POSTGRESQL_DATABASE_PASSWORD,
		'HOST': '127.0.0.1',
		'PORT': '5432',
	},
}
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


USE_I18N = True
USE_L10N = True

LANGUAGE_COOKIE_NAME = 'lang'

LANGUAGES = [
	('en', _('Английский')),
	('uk', _('Украинский')),
	('ru', _('Русский')),
]
LANGUAGE_CODE = 'ru-ru'
MODELTRANSLATION_DEFAULT_LANGUAGE = 'ru'
LOCALE_PATHS = [BASE_DIR / 'locale']


TIME_ZONE = 'UTC'
USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_DIRS = [
	BASE_DIR / 'constructor_telegram_bots/static',
	BASE_DIR / 'frontend/dist',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


os.makedirs(BASE_DIR / 'logs', exist_ok=True)

LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'formatters': {
		'verbose': {
			'format': '[{asctime}]: {levelname}: {name} > {funcName} || {message}',
			'style': '{',
		},
		'simple': {
			'format': '[{asctime}]: {message}',
			'style': '{',
		},
	},
	'handlers': {
		'console': {
			'level': 'INFO',
			'class': 'logging.StreamHandler',
			'formatter': 'simple',
		},
		'django_info_file': {
			'level': 'DEBUG',
			'class': 'logging.handlers.RotatingFileHandler',
			'filename': BASE_DIR / 'logs/django_info.log',
			'maxBytes': 10485760,
			'backupCount': 10,
			'formatter': 'verbose',
		},
		'django_error_file': {
			'level': 'WARNING',
			'class': 'logging.handlers.RotatingFileHandler',
			'filename': BASE_DIR / 'logs/django_error.log',
			'maxBytes': 10485760,
			'backupCount': 10,
			'formatter': 'verbose',
		},
	},
	'loggers': {
		'django': {
			'handlers': [
				'console',
				'django_info_file',
				'django_error_file',
			],
			'propagate': True,
		},
	},
}
