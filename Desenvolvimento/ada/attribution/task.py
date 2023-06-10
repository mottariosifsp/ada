import time
from datetime import datetime, timedelta
from time import sleep
from celery import Celery, shared_task

from attribution.views import professor_to_end_queue

app = Celery('tasks', broker='redis://localhost:6379')

@app.task
def times_up(professor):
    professor_to_end_queue(professor)
    return 

def schedule_task(seconds, professor):
    now = datetime.utcnow()
    sleep(seconds)
    times_up.apply_async(eta=now + timedelta(seconds=seconds), args=[professor])


app.conf.timezone = 'UTC'