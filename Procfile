release: python3 manage.py migrate
web: gunicorn FRESHOWBAND.wsgi --log-file -
worker: celery -A FRESHOWBAND worker