import os
from celery import Celery
from django.conf import settings

# set default Django settings module for 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PBEshop.settings')

app = Celery('PBEshop')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APS)