import os
from celery import Celery
# gource
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "setup.settings")
app = Celery("ada", broker_connection_retry_on_startup = True)
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()