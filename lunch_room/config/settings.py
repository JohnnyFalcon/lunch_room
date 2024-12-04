import os
from pathlib import Path
import environ
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env(
    DEBUG=(bool, False),
    SECRET_KEY=(str, ''),
    DATABASE_URL=(str, ''),
    EMAIL_HOST=(str, 'smtp.gmail.com'),
    EMAIL_PORT=(int, 587),
    EMAIL_HOST_USER=(str, ''),
    EMAIL_HOST_PASSWORD=(str, ''),
    EMAIL_USE_TLS=(bool, True),
    DEFAULT_FROM_EMAIL=(str, ''),
)

# Read .env file from Render's secret file location
environ.Env.read_env(os.path.join('/etc/secrets', '.env'))
# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = ['.onrender.com', 'localhost', '127.0.0.1']

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "login"

WHITENOISE_MIMETYPES = {
    '.css': 'text/css',
    '.js': 'application/javascript',
}

# Application definition
INSTALLED_APPS = [
    'lunch_room',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'config',
    'widget_tweaks',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this after SecurityMiddleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

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

# Database configuration for production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        **dj_database_url.config(
            default=env('DATABASE_URL'),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
}

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'lunch_room', 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

if os.environ.get('PROCESS_TYPE') != 'worker':
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = env.str('EMAIL_HOST', default='smtp.gmail.com')
    EMAIL_HOST_USER = env.str('EMAIL_HOST_USER', default='')
    EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD', default='')
    EMAIL_PORT = env.int('EMAIL_PORT', default=587)
    EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
    DEFAULT_FROM_EMAIL = env.str('DEFAULT_FROM_EMAIL', default=EMAIL_HOST_USER)