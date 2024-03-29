import os
from pathlib import Path
from dotenv import load_dotenv
import redis

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Нужно для быстрого доступа к id чата по SECRET_KEY без обращения к БД
REDIS = redis.Redis(host=os.getenv('REDIS_SK_HOST'), port=6379, db=0, decode_responses=True)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = os.getenv('DEBUG') in ['TRUE', 'true', '1', 'yes']

ANONYMIZE_DATA = (
    os.getenv('ANONYMIZE_DATA') in ['TRUE', 'True', 'true', '1', 'yes']
)

GMAIL_SEND_MESSAGE = (
    os.getenv('GMAIL_SEND_MESSAGE') in ['TRUE', 'True', 'true', '1', 'yes']
)

ALLOWED_HOSTS = ['127.0.0.1',
                 '0.0.0.0',
                 'localhost',
                 os.getenv('SERVER_IP'),
                 os.getenv('TEST_DOMAIN_NAME'),
                 os.getenv('PROD_DOMAIN_NAME'),  # прод всегда последний!
                 ]

CSRF_TRUSTED_ORIGINS = [f"https://{os.getenv('TEST_DOMAIN_NAME')}",
                        f"https://{os.getenv('PROD_DOMAIN_NAME')}"]

# Application definition

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'djoser',
    'rest_framework.authtoken',
    'corsheaders',
    'mail_templated',
    'api.apps.ApiConfig',
    'chats.apps.ChatsConfig',
    'users.apps.UsersConfig',
    'core.apps.CoreConfig',
    'channels',
    'storages',
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

# WSGI_APPLICATION = 'psyhelp.wsgi.application'
ASGI_APPLICATION = 'psyhelp.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('redis', 6379)],  # убрать в енв
        },
    },
}

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

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.getenv('REDIS_HOST'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
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
    'SEND_ACTIVATION_EMAIL': True,
    'ACTIVATION_URL': 'activate/{uid}/{token}/',
    'SERIALIZERS': {
        'user': 'api.serializers.UserSerializer',
        'user_list': 'api.serializers.UserSerializer',
        'user_create': 'api.serializers.UserCreateSerializer', },
    'LOGIN_FIELD': 'email',
    'PERMISSIONS': {
        'user': ['rest_framework.permissions.IsAuthenticated'],
        'user_create': ['api.permissions.IsAnonymous'],
        'user_list': ['api.permissions.IsModeratorOrAdmin'], },
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
if os.getenv('EMAIL_BACKEND') == 'SMTP':
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = BASE_DIR / 'sent_emails'
SERVER_EMAIL = 'from@example.com'

EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_USE_TLS = False
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MAX_EMAIL_LEN = 50
MAX_USER_LEN = 50

CHAT_SECRET_KEY_LENGTH = 20

CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')
CELERY_TASK_TRACK_STARTED = True
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

COMPRESS_IMAGE = os.getenv('COMPRESS_IMAGE') in ['TRUE', 'true', '1', 'yes']

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
CACHE_TTL = 1  # время хранение кеша в секундах

# количество последних сообщений вложенных в чат
LIMIT_MESSAGES = 2


AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'psyhelp.media'
AWS_S3_SIGNATURE_NAME = 's3v4',
AWS_S3_REGION_NAME = 'ru-central1'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_S3_VERITY = True
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_S3_ENDPOINT_URL = 'https://storage.yandexcloud.net'
