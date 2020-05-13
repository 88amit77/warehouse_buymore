import os
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'qwertyui1234567sdfghj'

DEBUG = True

ALLOWED_HOSTS = ['*', 'users_web']

INSTALLED_APPS = [
	'django.contrib.contenttypes',
	'django.contrib.auth',
	'django.contrib.staticfiles',
	'rest_framework',
	'rest_framework_swagger',
	'api',
	'djoser',
	'corsheaders'
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
		'NAME': 'users',
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
	'UNAUTHENTICATED_USER': None,
	'DEFAULT_AUTHENTICATION_CLASSES': [
		'rest_framework_simplejwt.authentication.JWTAuthentication',
	],
}

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

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, "static")

CORS_ORIGIN_ALLOW_ALL = True
