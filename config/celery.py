import os

from celery import Celery
from django.conf import settings

# set default Django settings module for 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")

# Use string here to avoid pickle issues.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Explicitly import tasks module so Celery registers tasks (do not autodiscover)
import src.infrastructure.messaging.tasks  # noqa: E402,F401

__all__ = ("app",)
