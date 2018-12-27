"""Django settings for uwsolar project.

For more information on this file, see https://docs.djangoproject.com/en/2.1/topics/settings/. For the full list of
settings and their values, see https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...).
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production. See
# https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/.

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'as9s7!##9kwbr2jkjxi5d*ps6(qn%i#@1iai&nab_k8r$d8e#-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'collector.apps.CollectorConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]

ROOT_URLCONF = 'uwsolar.urls'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages'
        ]
    }
}]

WSGI_APPLICATION = 'uwsolar.wsgi.application'

# Database. See https://docs.djangoproject.com/en/2.1/ref/settings/#databases.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
    }
}

# Password validation. See https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators.
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}
]

# Internationalization. See https://docs.djangoproject.com/en/2.1/topics/i18n/.
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images). See https://docs.djangoproject.com/en/2.1/howto/static-files/.
STATIC_URL = '/static/'

# Collector application config.
COLLECTOR_PANEL_HOST = '10.154.120.13'
COLLECTOR_METRICS_INPUT_WORKBOOK = 'collector/fixtures/nexus-metrics.xlsx'
COLLECTOR_METRICS_TOPIC_NAME_PREFIX = 'UW/Mercer/nexus_meter'
