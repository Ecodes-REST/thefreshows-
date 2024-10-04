from .common import *


DEBUG = True

SECRET_KEY = 'django-insecure-%)o322-!+kmy@dg38@=s_y!6w+$#=eoxfiyq9wa2i_hmfje6&f'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'FRESHOWBAND',
        'HOST': 'localhost',
        'PORT':'5432',
        'USER': 'emollz',
        'PASSWORD': 'Jr. Web Developer'
    }
}

STRIPE_SECRET_KEY = 'sk_test_51PYm9xHrfgZPwRJeEgKNOj0dc6E3DcnvVzVMTo6MjReeEi5iphzft1CPVDKVvQOXArBrD5vkZ0PRXIjwD7eHdJBm00NtVRu3az'


  