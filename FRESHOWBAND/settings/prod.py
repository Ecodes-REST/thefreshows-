import os
import dj_database_url
from .common import *

ALLOWED_HOSTS = ['freshowband.fly.dev/']

DEBUG = False

REDIS_URL= os.environ.get('REDIS_URL')
CELERY_BROKER_URL= REDIS_URL


DATABASES = {
    'default': dj_database_url.config(os.environ.get('DATABASE_URL')) 
}


if os.getenv('FLY_REGION') is None:
    # This is not a Fly.io deployment, so use the dev settings
    from .dev import *

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

SECRET_KEY= os.environ.get('SECRET_KEY')
STRIPE_SECRET_KEY= os.environ.get('STRIPE_SECRET_KEY')
STRIPE_PUBLISHABLE_KEY= os.environ.get('STRIPE_PUBLISHABLE_KEY')

#HTTPS settings
SESSION_COOKIE_SECURE= True
CSRF_COOKIE_SECURE= True