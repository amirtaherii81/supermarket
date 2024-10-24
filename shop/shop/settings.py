"""
Django settings for shop project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-oh_qn1x2&^1au0ljoc6t6z@cjiyi4=_k-1d$0rn-*m#ckp_0t)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = []

# DEBUG = False
# ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.main.apps.MainConfig',
    'apps.accounts.apps.AccountsConfig',
    'apps.products.apps.ProductsConfig',
    'apps.orders.apps.OrdersConfig',
    'apps.discounts.apps.DiscountsConfig',
    'apps.payments.apps.PaymentsConfig',
    'apps.warehouses.apps.WarehousesConfig',
    'apps.comment_scoring_favorites.apps.CommentScoringFavoritesConfig',
    'apps.search.apps.SearchConfig',
    'apps.test_api.apps.TestApiConfig',
    # Add foreign key application
    'django_admin_listfilter_dropdown',
    'ckeditor',
    'ckeditor_uploader',
    'django_render_partial',
    'django.contrib.humanize',  # اپ پیشفرض جنگو
    'django_filters',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'middlewares.middleware.RequestMiddleware',
]

ROOT_URLCONF = 'shop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates/')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.main.views.media_admin'
            ],
        },
    },
]


WSGI_APPLICATION = 'shop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'mysql.connector.django',
        'NAME': 'supermarket4',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '3306'
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'fa-ir'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static/'),)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = "accounts.CustomUser" # nameApp & nameClass



CKEDITOR_UPLOAD_PATH = "images/ckeditor/upload_files/"
CKEDITOR_STORAGE_BACKEND = "django.core.files.storage.FileSystemStorage"
CKEDITOR_CONFIGS = {
    'default': 
        {
        'toolbar': 'Custom',
        'toolbar_Custom': [
                ['Bold', 'link', 'Unlink', 'Image'],
            ],
        },
    'special': 
        {
            'toolbar': 'Special', 'height': 500,
            'toolbar': 'full',
            'toolbar_Special':
                [
                    ['Bold', 'Link', 'Unlink', 'Image'],
                    ['CodeSnippet'], # here
                ],  'extraplugins': ','.join(['codesnippet', 'clipboard', ]) # here
        },
    'special_an':
        {'toolbar': 'Special', 'height':500,
         'toolbar_Special':
            [
                ['Bold'],
                ['CodeSnippet'],
            ], 'extraplugins': ','.join(['codesnippet', ])  # here
        }
}