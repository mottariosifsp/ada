from celery import Celery, shared_task

app = Celery('tasks', broker='redis://localhost:6379')

@app.task
def helloworld():
    return print('rodando tarefa helloworld: OK')

app.conf.timezone = 'UTC'