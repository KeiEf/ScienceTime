import os
from pathlib import Path
import django_heroku
from decouple import config as env_config
#from decouple import Config, RepositoryEnv # ← 追加
import sys 

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env_config('SECRET_KEY')
DEBUG = env_config('ST_DEBUG', default=False, cast=bool)
MAINTENANCE_MODE = env_config('ST_MAINTENANCE', default=False, cast=bool)

#----- HTTPS ----- 
SECURE_SSL_REDIRECT = not ('runserver' in sys.argv)
#SECURE_SSL_REDIRECT = False
ALLOWED_HOSTS = ['www.sciencetime.jp', 'sciencetime.jp', 'sciencetime.herokuapp.com', 'localhost', '127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary', 
    'cloudinary_storage',
    'website','taggit',
    'captcha', 
    'members'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'website.core.middleware.MaintenanceModeMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env_config('DB_NAME'),
        'USER': env_config('DB_USER'),
        'PASSWORD': env_config('DB_PASSWORD'),
        'HOST': env_config('DB_HOST', default='localhost'),
        'PORT': env_config('DB_PORT', default='5432'),
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


LANGUAGE_CODE = 'ja'
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_L10N = True
USE_TZ = True
ALLOW_UNICODE_SLUGS = True
X_FRAME_OPTIONS = 'ALLOW'

STATIC_URL = '/static/'
#STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
	os.path.join(BASE_DIR, 'static')
]
#STATICFILES_DIRS = [
#    os.path.join(BASE_DIR, 'staticfiles')  # Use a different directory for development
#]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
MEDIA_URL = '/media/'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGIN_REDIRECT_URL ="index"
LOGOUT_REDIRECT_URL ="index"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

#問合せメール受信設定
##EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' 
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = env_config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env_config('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True

RECAPTCHA_PRIVATE_KEY = env_config('RECAPTCHA_PRIVATE_KEY')
RECAPTCHA_PUBLIC_KEY = env_config('RECAPTCHA_PUBLIC_KEY')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

if not DEBUG:
    django_heroku.settings(locals())

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': env_config('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': env_config('CLOUDINARY_API_KEY'),
    'API_SECRET': env_config('CLOUDINARY_API_SECRET'),
}

