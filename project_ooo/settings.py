""" docstring """
from datetime import timedelta
from pathlib import Path
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    ####### django-cors-headers #######
    'corsheaders',
    ####### project app #######
    'users',
    'articles',
    'challenges',
    'achievements',
    'social_auth',
    'utils',
    ####### django rest framework #######
    'drf_yasg',
    'rest_framework',
    # 'rest_framework_simplejwt',
    # 'rest_framework.authtoken',
    # # dj_rest_auth
    # 'dj_rest_auth',
    # 'dj_rest_auth.registration',
    # # django-allauth
    # 'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}

# Refs https://pypi.org/project/django-cors-headers/

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5500",
    "http://localhost:3000",
    "http://127.0.0.1:8080",
    "https://tomatopizza.github.io",
]

####### 날씨 API 관련 #######
WEATHER_KEY = os.environ.get("WEATHER_KEY")

####### 사이트 관련 #######
# SITE_ID = 1

####### 이메일 인증 관련 #######
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER") #sender's email-id
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD") #password associated with above email-id
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# ACCOUNT_CONFIRM_EMAIL_ON_GET = True
# ACCOUNT_EMAIL_REQUIRED = True

# ACCOUNT_EMAIL_VERIFICATION = "mandatory"
# ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
# LOGIN_REDIRECT_URL = "https://tomatopizza.github.io/template/index.html"

###### 소셜 계정 관련 #######
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
#     # Needed to login by username in Django admin, regardless of `allauth`
#     'allauth.account.auth_backends.AuthenticationBackend', # <- OAuth 필수 #
#     # `allauth` specific authentication methods, such as login by e-mail
]

# SOCIALACCOUNT_LOGIN_ON_GET = True

# SOCIALACCOUNT_PROVIDERS = { # Provider specific settings
#     "google": {
#         "SCOPE": [
#             "profile",
#             "email",
#         ],
#         "AUTH_PARAMS": {
#             "access_type": "online",
#         },
#         "APP": {
#             "client_id": str(os.environ.get("GOOGLE_CLIENT_ID")),
#             "secret": str(os.environ.get("GOOGLE_CLIENT_SECRET")),
#             "key": "",
#         },
#     }
# }

REST_FRAMEWORK = {

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination', 
    'PAGE_SIZE': 10,
    'NON_FIELD_ERRORS_KEY': 'error',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
    # 'DEFAULT_PARSER_CLASSES': (
    #     # Specifies the parser used when accessing request.data properties.
    #     'rest_framework.parsers.JSONParser',
    #     'rest_framework.parsers.FormParser',
    #     'rest_framework.parsers.MultiPartParser'
    # )
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=720),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
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

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', # ! carefull the location CorsMiddleware
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project_ooo.urls'

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

WSGI_APPLICATION = 'project_ooo.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_USER_MODEL = 'users.User'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_ROOT = BASE_DIR /  "static"
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
# MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"
