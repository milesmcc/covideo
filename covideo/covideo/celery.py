import logging
import os

import celery
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "covideo.settings")

app = Celery("covideo", broker=settings.CELERY_BROKER_URL)

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()