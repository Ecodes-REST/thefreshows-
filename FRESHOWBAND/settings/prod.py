import os
from .common import *

ALLOWED_HOSTS = []

DEBUG = False

SECRET_KEY= os.environ['SECRET_KEY']
STRIPE_SECRET_KEY= os.environ['STRIPE_SECRET_KEY']
STRIPE_PUBLISHABLE_KEY= os.environ['STRIPE_PUBLISHABLE_KEY']