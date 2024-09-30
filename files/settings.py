"""
Django settings for files project.

Generated by 'django-admin startproject' using Django 4.2.16.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent



# Build paths for media - local
# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Static files (CSS, JavaScript, Images) - local
# https://docs.djangoproject.com/en/4.2/howto/static-files/
# STATIC_URL = 'static/'
# STATIC_ROOT = 'static'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-@z6wj!5hrz7gys%u^k8()0ijw5!g8#)9jl$5j(55rdvr#a^3%$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# add endpoints here
ALLOWED_HOSTS = ['127.0.0.1', 'FilesHosting-env-1.eba-n5rjbfw3.us-east-2.elasticbeanstalk.com']


# Application definition

INSTALLED_APPS = [
    'storages',
    'files',
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

ROOT_URLCONF = 'files.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'files.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# local db setup 
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# postgres db setup 
DB_HOSTNAME = os.environ.get('RDS_HOSTNAME')
# DB_PORT = os.environ.get('RDS_PORT')
DB_NAME = os.environ.get('RDS_DB_NAME')
DB_USERNAME = os.environ.get('RDS_USERNAME')
DB_PASSWORD = os.environ.get('RDS_PASSWORD')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DB_NAME,                      
        'USER': DB_USERNAME,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOSTNAME,
        # 'PORT': DB_PORT,
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# AWS S3 Setup 
# Don't need these two since we have set it up in the config (~/.aws/credentials)
# AWS_ACCESS_KEY_ID = '' 
# AWS_SECRET_ACCESS_KEY = '' 

# Basic Storage configuration for Amazon S3 (Irrespective of Django versions)
# AWS_S3_SESSION_PROFILE = 'eb-cli'
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_FILE_OVERWRITE = False
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}

STORAGES = {
    # Media file (image) management   
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3StaticStorage",
        'OPTIONS': {
            'bucket_name': AWS_STORAGE_BUCKET_NAME,
            'location': 'media',
        }
    },
    
    # CSS and JS file management
    "staticfiles": {
        "BACKEND": "storages.backends.s3boto3.S3StaticStorage",
        'OPTIONS': {
            'bucket_name': AWS_STORAGE_BUCKET_NAME,
            'location': 'static',
        }
    },
}

# Set up path for media and static folders - s3 
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
# MEDIA_ROOT = AWS_S3_CUSTOM_DOMAIN
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
# STATIC_ROOT = AWS_S3_CUSTOM_DOMAIN