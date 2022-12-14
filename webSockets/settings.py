
from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent.parent



SECRET_KEY = 'django-insecure-nb87-(2x3@&06b+0*y$iq2m95y9g^q)&n03*k$9&xilf+j-hpp'

DEBUG = True

ALLOWED_HOSTS = ['*']



INSTALLED_APPS = [
    'channels',
    'crispy_forms',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'base',
]

ASGI_APPLICATION = 'webSockets.asgi.application'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'webSockets.urls'

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

WSGI_APPLICATION = 'webSockets.wsgi.application'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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


CHANNEL_LAYERS = {
    'default':{
        'BACKEND':'channels.layers.InMemoryChannelLayer'
    }
}


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Istanbul'


USE_I18N = True


USE_TZ = True


CRISPY_TEMPLATE_PACK = 'bootstrap4'


STATIC_ROOT= os.path.join(BASE_DIR,'staticfiles')


STATIC_URL = '/static/'


MEDIA_ROOT = 'media/'


MEDIA_URL = 'media/'



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
