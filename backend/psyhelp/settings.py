import os
from pathlib import Path
from dotenv import load_dotenv
import redis

load_dotenv()
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS = redis.Redis(host=REDIS_HOST, port=6379, db=0, decode_responses=True)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = os.getenv('DEBUG') in ['TRUE', 'true', '1', 'yes']

ALLOWED_HOSTS = ['127.0.0.1',
                 '0.0.0.0',
                 'localhost',
                 os.getenv('SERVER_IP'),
                 os.getenv('TEST_DOMAIN_NAME'),
                 os.getenv('PROD_DOMAIN_NAME'),  # прод всегда последний!
                 ]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'djoser',
    'rest_framework_simplejwt',
    'rest_framework.authtoken',
    'corsheaders',
    'mail_templated',
    'api.apps.ApiConfig',
    'chats.apps.ChatsConfig',
    'users.apps.UsersConfig',
    'core.apps.CoreConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'psyhelp.urls'

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

WSGI_APPLICATION = 'psyhelp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}

AUTH_USER_MODEL = 'users.CustomUser'
AUTHENTICATION_BACKENDS = ['users.backends.EmailBackend']


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'collected_static'
MEDIA_URL = '/media/'
MEDIA_ROOT = '/media'  # в докере проще так
# MEDIA_ROOT = BASE_DIR / 'media'  # для отладки

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100
}
PAGE_SIZE = 6

DJOSER = {
    'SERIALIZERS': {
        'user': 'api.serializers.UserSerializer',
        'user_list': 'api.serializers.UserSerializer',
        'user_create': 'api.serializers.UserCreateSerializer', },
    'LOGIN_FIELD': 'email',
    'PERMISSIONS': {
        'user': ['rest_framework.permissions.IsAuthenticated'],
        'user_list': ['rest_framework.permissions.IsAuthenticated'], },
    'HIDE_USERS': False,
    'PASSWORD_RESET_CONFIRM_URL': 'reset-confirmation/{uid}/{token}/',
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': 'True',
}

CORS_URLS_REGEX = r'^/api/.*$'

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://' + os.getenv('TEST_DOMAIN_NAME'),
    'https://' + os.getenv('TEST_DOMAIN_NAME'),
    'http://' + os.getenv('PROD_DOMAIN_NAME'),
    'https://' + os.getenv('PROD_DOMAIN_NAME'),
]

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = BASE_DIR / 'sent_emails'
SERVER_EMAIL = 'from@example.com'

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_USE_TLS = False
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


MAX_EMAIL_LEN = 50
MAX_USER_LEN = 50

CHAT_SECRET_KEY_LENGTH = 20

COMPRESS_IMAGE = True
