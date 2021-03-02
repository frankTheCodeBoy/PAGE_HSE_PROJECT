"""
Django settings for tango_rango project.

Generated by 'django-admin startproject' using Django 3.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
from os import path, environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = path.join(BASE_DIR, 'templates')
MEDIA_DIR = path.join(BASE_DIR, 'media')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
with open('tango_rango/my_safe.txt') as f:
    SECRET_KEY = f.read().strip()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    # My Apps.
    'rango_app',
    'registration',
    'bootstrap4',
    'django_heroku',
    # Default django apps.
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tango_rango.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR,],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'tango_rango.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Registration, Login settings
REGISTRATION_OPEN = True
ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_AUTO_LOGIN = True
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = "/accounts/login/"

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATIC_ROOT = path.join(BASE_DIR, "staticfiles")
STATIC_URL = '/static/'
MEDIA_ROOT = MEDIA_DIR
MEDIA_URL = '/media/'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Logging
LOGGING = {
'version': 1,
'disable_existing_loggers': False,
'formatters': {
    'verbose': {
        'format': ('%(asctime)s [%(process)d] [%(levelname)s] '
                   'pathname=%(pathname)s lineno=%(lineno)s '
                   'funcname=%(funcName)s %(message)s'),
        'datefmt': '%Y-%m-%d %H:%M:%S'
    },
    'simple': {
        'format': '%(levelname)s %(message)s'
    }
},
'handlers': {
    'null': {
        'level': 'DEBUG',
        'class': 'logging.NullHandler',
    },
    'console': {
        'level': 'INFO',
        'class': 'logging.StreamHandler',
        'formatter': 'verbose'
    }
},
'loggers': {
    'django': {
        'handlers': ['console'],
        'level': 'DEBUG',
        'propagate': True,
    },
    'django.request': {
        'handlers': ['console'],
        'level': 'DEBUG',
        'propagate': False,
    },
}}

import django_heroku
django_heroku.settings(config=locals(), staticfiles=False, logging=False)
