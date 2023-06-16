from multiprocessing.pool import AsyncResult
import time
from datetime import datetime, timedelta
from time import sleep
from celery import Celery, shared_task
from area.models import Blockk
from user.models import User
from attribution import views

# from attribution.views import professor_to_end_queue

app = Celery('tasks', broker='redis://localhost:6379')

task = None

@app.task
def times_up(professor_id, blockk_id):
    professor = User.objects.get(id=professor_id)
    blockk = Blockk.objects.get(id=blockk_id)
    views.professor_to_end_queue(professor)
    views.start_attribution(blockk)

def schedule_task(seconds, professor, blockk):
    now = datetime.utcnow()
    global task
    print(f'{professor} tem {seconds} segundos para responder')
    task = times_up.apply_async(eta=now + timedelta(seconds=seconds), args=[professor.id, blockk.id])

async def cancel_scheduled_task():
    global task
    if task and task.state == 'PENDING':
        task.revoke(terminate=True)
        return True
    return False

app.conf.timezone = 'UTC'