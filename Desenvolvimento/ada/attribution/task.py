from multiprocessing.pool import AsyncResult
import time
from datetime import datetime, timedelta
from time import sleep
from celery import Celery, shared_task

from attribution import views

# from attribution.views import professor_to_end_queue

app = Celery('tasks', broker='redis://localhost:6379')

task = None

@app.task
def times_up(professor):
    views.professor_to_end_queue(professor)
    return 

def schedule_task(seconds, professor):
    now = datetime.utcnow()
    global task
    task = times_up.apply_async(eta=now + timedelta(seconds=seconds), args=[professor])

async def cancel_scheduled_task():
    global task
    if task and task.state == 'PENDING':
        task.revoke(terminate=True)
        return True
    return False

app.conf.timezone = 'UTC'