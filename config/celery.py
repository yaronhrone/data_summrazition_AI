import os
from celery import Celery
from celery.signals import worker_ready
from django.db import connections
from django.db.utils import OperationalError

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@worker_ready.connect
def at_start(sender, **kwargs):
    from articles.tasks import fetch_nyt_articles_task

    fetch_nyt_articles_task.delay("technology")