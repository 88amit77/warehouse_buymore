import os
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'qwertyui1234567sdfghj'

DEBUG = True

ALLOWED_HOSTS = ['*', 'warehouse_web']

INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_yasg',
    'api',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'api.urls'

WSGI_APPLICATION = 'api.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'warehouse',
        'USER': 'postgres',
        'PASSWORD': 'buymore2',
        'HOST': 'buymore2.cegnfd8ehfoc.ap-south-1.rds.amazonaws.com',
        'PORT': '',
    },
    'orders': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'orders',
        'USER': 'postgres',
        'PASSWORD': 'buymore2',
        'HOST': 'buymore2.cegnfd8ehfoc.ap-south-1.rds.amazonaws.com',
        'PORT': '',
    },
    'products': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'products',
        'USER': 'postgres',
        'PASSWORD': 'buymore2',
        'HOST': 'buymore2.cegnfd8ehfoc.ap-south-1.rds.amazonaws.com',
        'PORT': '',
    }
}

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('Bearer',),

    'USER_ID_FIELD': 'id',
    'PAYLOAD_ID_FIELD': 'user_id',

    'TOKEN_LIFETIME': timedelta(days=1),
    'TOKEN_REFRESH_LIFETIME': timedelta(days=7),

    'SIGNING_KEY': SECRET_KEY,  # Default to the django secret key

    'TOKEN_BACKEND': 'rest_framework_simplejwt.backends.TokenBackend',
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

REST_FRAMEWORK = {
    'UNAUTHENTICATED_USER': None
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
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

STATIC_URL = '/warehouse/static/'

STATIC_ROOT = os.path.join(BASE_DIR, "static")

CORS_ORIGIN_ALLOW_ALL = True

CRONJOBS = [
    ('* * * * *', '.picklist.cron.generate_picklist', '>> /home/pace/Documents/python/Buymore 2.0/Warehouse/file.log'),
]


# Dropbox storage
DEFAULT_FILE_STORAGE = 'storages.backends.dropbox.DropBoxStorage'
DROPBOX_OAUTH2_TOKEN = 'd7ElXR2Sr-AAAAAAAAAAC2HC0qc45ss1TYhRYB4Jy6__NJU1jjGiffP7LlP_2rrf'
DROPBOX_ROOT_PATH = '/buymore2'
