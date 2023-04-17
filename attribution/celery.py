
import os
from celery import Celery
from django.conf import settings



# Define o nome do projeto Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')

app = Celery('attribution')

# Configurações do Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Carrega as tarefas do diretório 'tasks' de cada aplicação Django
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'check-button-every-10-seconds': {
        'task': 'attribution.tasks.check_button_pressed',
        'schedule': 10.0
    },
}
