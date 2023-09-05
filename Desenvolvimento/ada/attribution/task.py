from multiprocessing.pool import AsyncResult
import time
from datetime import datetime, timedelta
from time import sleep
from celery import Celery, shared_task
import redis
from area.models import Blockk
from user.models import User
from attribution import views

# from attribution.views import professor_to_end_queue

app = Celery('tasks', broker='redis://localhost:6379')

redis_client = redis.Redis(host='localhost', port=6379)

i = app.control.inspect()

@app.task
def finalization_deadline_start():
    print("finalization_deadline_start")

@app.task
def attribution_deadline_start(blockk_id):
    blockk = Blockk.objects.get(registration_block_id=blockk_id)
    views.start_attribution(blockk)
    views.remove_professors_without_preference(blockk)
    print("attribution_deadline_start")

@app.task
def attribution_preference_deadline_start():
    print("attribution_preference_deadline_start")

def schedule_deadline(task, dateperiod, name, queue, *args):
    now_today = datetime.today()
    now = datetime.utcnow()
    eta = (dateperiod - now_today).total_seconds()
    regis_task = task.apply_async(eta=now + timedelta(seconds=eta), args=list(args), queue=queue)
    redis_client.set(name, regis_task.id)

@app.task
def times_up(professor_id, blockk_id):
    professor = User.objects.get(id=professor_id)
    blockk = Blockk.objects.get(id=blockk_id)
    views.timestup(professor, blockk)
    print(f'Tempo do professor {professor} acabou!')

def schedule_task(seconds, professor, blockk):
    i.scheduled()
    i.active()

    now = datetime.utcnow()
    eta = now + timedelta(seconds=seconds)
    task = times_up.apply_async(eta=now + timedelta(seconds=seconds), args=[professor.id, blockk.id])
    # Store task information in Redis
    redis_client.set('task', task.id)
    redis_client.set('task_eta', eta.isoformat())

    print(f'Professor {professor} tem {seconds} segundos para escolher suas novas aulas')

def cancel_scheduled_task(name):
    task_id = redis_client.get(name)
    if task_id:
        task = app.AsyncResult(bytes.decode(task_id, 'utf-8'))
        task.revoke(terminate=True)
        print(task)
        redis_client.delete(name)
        return True
    return False

def get_time_left():
    task_eta = redis_client.get('task_eta')
    if task_eta:
        eta = datetime.fromisoformat(task_eta.decode())
        now = datetime.utcnow()
        time_left = eta - now
        return time_left.total_seconds()
    return None

def cancel_all_tasks():
    print('excluindo tarefas')
    # Obtém a lista de tarefas (tasks) ativas
    active_tasks = app.control.inspect().scheduled()
    print(active_tasks)
    # Cancela cada tarefa ativa usando a função revoke()
    for worker, tasks in active_tasks.items():
        for task in tasks:
            task.revoke(terminate=True)


app.conf.timezone = 'UTC'