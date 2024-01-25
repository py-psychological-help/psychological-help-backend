import os

from celery import Celery

# На ревью. Здесь подключается Celery 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'psyhelp.settings')

app = Celery('psyhelp')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
