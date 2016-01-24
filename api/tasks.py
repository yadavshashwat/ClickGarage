from mailing import views as mViews
from celery import Celery

BROKER_URL = 'redis://localhost:6379/0'
