from decouple import config
from .base import *


APP_URL = "http://localhost:3000"
HOST_URL = "http://127.0.0.1:8000"

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# CORS

CORS_ALLOW_ALL_ORIGINS = True
