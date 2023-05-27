from celery import Celery, shared_task

app = Celery('tasks', broker='redis://localhost:6379')

app.conf.timezone = 'UTC'