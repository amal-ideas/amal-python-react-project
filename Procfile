web: gunicorn application.wsgi --log-file -
worker: celery -A application worker
beat: celery -A application beat -S django