from .common import *
import dj_database_url


DEBUG = True

SECRET_KEY = 'django-insecure-%)o322-!+kmy@dg38@=s_y!6w+$#=eoxfiyq9wa2i_hmfje6&f'


DATABASES = {
    'default': dj_database_url.config(default=os.getenv('DATABASE_URL'), conn_max_age=600)
}

STRIPE_SECRET_KEY = 'sk_test_51PYm9xHrfgZPwRJeEgKNOj0dc6E3DcnvVzVMTo6MjReeEi5iphzft1CPVDKVvQOXArBrD5vkZ0PRXIjwD7eHdJBm00NtVRu3az'


  