import time
from datetime import datetime, timedelta
from time import sleep
from celery import Celery, shared_task

app = Celery('tasks', broker='redis://localhost:6379')

@app.task
def olamundo():
    return print('rodando tarefa a cada 5 segundos: OK')

@shared_task
def printas():
    return print('agendamento de tarefa: OK')

def agendar_tarefa():
    now = datetime.utcnow()
    printas.apply_async(eta=now + timedelta(seconds=10.0))


app.conf.timezone = 'UTC'