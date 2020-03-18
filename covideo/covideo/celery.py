import logging
import os

import celery
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

logger = logging.getLogger(__name__)


@celery.signals.task_failure.connect
def on_task_failure(**kwargs):
    logger.exception(
        f"task {kwargs['task_id']} failed with exception", exc_info=kwargs["exception"]
    )


@celery.signals.task_success.connect
def on_task_success(**kwargs):
    logger.info(f"task {kwargs['task_id']} completed successfully")


@celery.signals.task_received.connect
def on_task_received(**kwargs):
    print(f"task {kwargs['task_id']} received")


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "covideo.settings")

app = Celery("covideo", broker=settings.CELERY_BROKER_URL)

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()