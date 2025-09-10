# oldtree_project/settings.py

import os
from pathlib import Path
import environ  # Import environ

# Initialize environ
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# --- SECURITY SETTINGS ---
# Use the SECRET_KEY from our environment variables
SECRET_KEY = env('SECRET_KEY')

# Use the DEBUG value from our environment variables
DEBUG = env('DEBUG')

# Configure ALLOWED_HOSTS. We'll add our Render URL later.
# For now, it's empty in production, but we'll add localhost for local dev.
ALLOWED_HOSTS = []

RENDER_EXTERNAL_HOSTNAME = env.str('RENDER_EXTERNAL_HOSTNAME', default=None)
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
    
if not DEBUG:
    # Add localhost if you want to run with DEBUG=False locally
    # e.g., python manage.py runserver --settings=oldtree_project.settings
    ALLOWED_HOSTS.append('127.0.0.1')


# --- APPLICATION DEFINITION ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic', # Add whitenoise
    'django.contrib.staticfiles',
    
    # 3rd Party Apps
    'rest_framework',

    # Local Apps
    'stock_api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Add whitenoise middleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'oldtree_project.urls'

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

WSGI_APPLICATION = 'oldtree_project.wsgi.application'


# --- DATABASE CONFIGURATION ---
# Use the DATABASE_URL from our environment variables,
# falling back to our local SQLite database if it's not set.
DATABASES = {
    'default': env.db('DATABASE_URL', default=f'sqlite:///{BASE_DIR}/db.sqlite3')
}


# --- PASSWORD VALIDATION ---
AUTH_PASSWORD_VALIDATORS = [
    # ... (Keep the existing validators) ...
]


# --- INTERNATIONALIZATION ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# --- STATIC FILES (CSS, JavaScript, Images) ---
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# --- DEFAULT PRIMARY KEY FIELD TYPE ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'