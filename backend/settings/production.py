from .base import *
from decouple import config


APP_URL = ""
HOST_URL = ""

DEBUG = False

ALLOWED_HOSTS = ['localhost']


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# CORS

CORS_ALLOWED_ORIGINS = [
]
