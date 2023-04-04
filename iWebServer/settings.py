"""
Django settings for iWebServer project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
import sys
from datetime import timedelta
from pathlib import Path
from interface.config import iWebServerBaseConfig
from django.utils.translation import gettext_lazy as _


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-**qs6ui9h%oae9ks)boqjy#644fwdgtcpb6eh73210y%*fepv='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = iWebServerBaseConfig.IWEBSERVER_APP_DEBUG

ALLOWED_HOSTS = ['*']
# CSRF_TRUSTED_ORIGINS = ['http://localhost:4000']
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760

# for allauth
SITE_ID = 1

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Application definition

INSTALLED_APPS = [
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'myaccount',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'guardian',
    'rest_framework',
    'rest_framework_simplejwt',
    'channels',
    'crispy_forms',
    'crispy_bootstrap4',
    #'corsheaders',

    'interface',
    'websocket',
#########################################################
    'pcd',
#########################################################
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'corsheaders.middleware.CorsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
)

ROOT_URLCONF = 'iWebServer.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
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

WSGI_APPLICATION = 'iWebServer.wsgi.application'
ASGI_APPLICATION = 'iWebServer.routing.application'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        "rest_framework.permissions.IsAuthenticated",
        # 'rest_framework_simplejwt.authentication.JWTAuthentication'
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser"
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTTokenUserAuthentication',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=int(iWebServerBaseConfig.IWEBSERVER_JWT_ACCESS_TOKEN_LIFETIME_DAYS),
                                       seconds=int(iWebServerBaseConfig.IWEBSERVER_JWT_ACCESS_TOKEN_LIFETIME_SECONDS),
                                       hours=int(iWebServerBaseConfig.IWEBSERVER_JWT_ACCESS_TOKEN_LIFETIME_HOURS),
                                       minutes=int(iWebServerBaseConfig.IWEBSERVER_JWT_ACCESS_TOKEN_LIFETIME_MINUTES),
                                       weeks=int(iWebServerBaseConfig.IWEBSERVER_JWT_ACCESS_TOKEN_LIFETIME_WEEKS)),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=365),
}

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': iWebServerBaseConfig.IWEBSERVER_DB_MYSQL_DBNAME,
        'USER': iWebServerBaseConfig.IWEBSERVER_DB_MYSQL_USER,
        'PASSWORD': iWebServerBaseConfig.IWEBSERVER_DB_MYSQL_PASSWORD,
        'HOST': iWebServerBaseConfig.IWEBSERVER_DB_MYSQL_HOST,
        'PORT': iWebServerBaseConfig.IWEBSERVER_DB_MYSQL_PORT,
        'OPTIONS': {'charset': 'utf8mb4', 'ssl_mode': 'DISABLED'} if (sys.version[:5] == "3.10." and sys.platform.startswith('linux')) else {'charset': 'utf8mb4'},
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

LANGUAGES = (
    ('zh-hans', _('Simplified Chinese')),
    ('zh-hant', _('Traditional Chinese')),
    ('en-us', _('English')),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_TZ = True

MENU_NEED_URL = {}

#CORS_ALLOW_ALL_ORIGINS = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES = os.path.join(BASE_DIR, 'static')
STATIC_FC_URL = STATIC_URL

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

SIMPLEUI_HOME_INFO = False

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

# django-allauth
# ------------------------------------------------------------------------------
# ACCOUNT_ALLOW_REGISTRATION = True
# ACCOUNT_ALLOW_REGISTRATION = False
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_AUTHENTICATION_METHOD = 'username'
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_EMAIL_REQUIRED = True
# https://django-allauth.readthedocs.io/en/latest/configuration.html
# ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_VERIFICATION = 'none'

ACCOUNT_SIGNUP_FORM_CLASS = 'myaccount.forms.SignupForm'

# AUTHENTICATION
# ------------------------------------------------------------------------------
LOGIN_REDIRECT_URL = '/'

# http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = 'bootstrap4'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# LOGGING = {
#     'version': 1,  # 保留字
#     'disable_existing_loggers': False,  # 禁用已经存在的logger实例
#     # 日志文件的格式
#     'formatters': {
#         # 详细的日志格式
#         'standard': {
#             'format': '[%(levelname)s][%(asctime)s][%(threadName)s:%(thread)d][%(name)s][%(funcName)s:%(lineno)d]%(message)s'
#         },
#         # 简单的日志格式
#         'simple': {
#             'format': '[%(levelname)s][%(threadName)s][%(asctime)s]%(message)s'
#         },
#         # 定义一个特殊的日志格式
#         'collect': {
#             'format': '%(message)s'
#         }
#     },
#     # 过滤器
#     'filters': {
#         'require_debug_true': {
#             '()': 'django.utils.log.RequireDebugTrue',
#         },
#     },
#     # 处理器
#     'handlers': {
#         # 在终端打印
#         'console': {
#             'level': 'DEBUG',
#             'filters': ['require_debug_true'],  # 只有在Django debug为True时才在屏幕打印日志
#             'class': 'logging.StreamHandler',  #
#             'formatter': 'standard'
#         },
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.handlers.TimedRotatingFileHandler',
#             'filename': '{}/iwebserver_v1.log'.format(iWebServerBaseConfig.IWEBSERVER_LOG_DIR),
#             'formatter': 'standard',
#             'when': 'W0',
#             'interval': 1,
#             'backupCount': 12,
#             'encoding': 'utf-8'
#         },
#     },
#     'loggers': {
#         # 默认的logger应用如下配置
#         '': {
#             'handlers': ['file', 'console'],  # 上线之后可以把'console'移除
#             'level': 'INFO',
#             'propagate': True,  # 向不向更高级别的logger传递
#         },
#     },
# }