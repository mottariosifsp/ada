from multiprocessing import AuthenticationError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, render
from user.models import User
from django.http import HttpResponseServerError
import sys
import logging
import traceback
from pathlib import Path
from django.contrib.auth import logout

def login(request):
    if request.method == 'POST':
        form = AuthenticationError(request, data=request.POST)
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

@login_required
def home(request):
    if request.user.is_staff and not request.user.is_professor and not request.user.is_superuser:
        return redirect('home_staff')
    elif request.user.is_professor and not request.user.is_staff and not request.user.is_superuser:
        return redirect('home_professor')
    else:
        return render(request, 'user/home.html')
    

def signup(request):
    return render(request, 'registration/signup.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def handler404(request, exception):

    #MUDAR
    log_directory = Path.home() / 'Documents' / 'logs'
    log_directory.mkdir(parents=True, exist_ok=True)
    log_file_path = log_directory / 'error.log'

    custom_logger = logging.getLogger('custom_logger')
    custom_handler = logging.FileHandler(log_file_path)
    custom_handler.setFormatter(CustomFormatter())
    custom_logger.addHandler(custom_handler)
    custom_logger.setLevel(logging.ERROR)

    user = request.user if hasattr(request, 'user') else None
    if user and user.is_authenticated:
        user_info = f'User: {user.first_name}'
    else:
        user_info = f'IP: {request.META["REMOTE_ADDR"]}' if hasattr(request, 'META') and 'REMOTE_ADDR' in request.META else 'IP: N/A'

    custom_logger.error("Erro 404 - %s - Página não encontrada: %s", user_info, request.path)

    return render(request, 'error/404.html', status=404)


def handler500(request):

    # MUDAR
    log_directory = Path.home() / 'Documents' / 'logs'
    log_directory.mkdir(parents=True, exist_ok=True)
    log_file_path = log_directory / 'error.log'

    custom_logger = logging.getLogger('custom_logger')
    custom_handler = logging.FileHandler(log_file_path)
    custom_handler.setFormatter(CustomFormatter())
    custom_logger.addHandler(custom_handler)
    custom_logger.setLevel(logging.ERROR)

    exc_type, exc_value, exc_traceback = sys.exc_info()

    user = request.user if hasattr(request, 'user') else None
    if user and user.is_authenticated:
        user_info = f'User: {user.first_name}'
    else:
        user_info = f'IP: {request.META["REMOTE_ADDR"]}' if hasattr(request, 'META') and 'REMOTE_ADDR' in request.META else 'IP: N/A'

    custom_logger.error("Erro 500 - %s - Tipo de Exceção: %s, Mensagem: %s", user_info, exc_type.__name__, str(exc_value))

    return render(request, 'error/500.html', status=500)

def provocar_erro_500(request):
    raise Exception("Erro 500 forçado - Internal Server Error")


class CustomFormatter(logging.Formatter):
    def format(self, record):
        user = record.request.user if hasattr(record, 'request') and hasattr(record.request, 'user') else None
        if user and user.is_authenticated:
            user_info = f'User: {user.first_name}'
        else:
            user_info = f'IP: {record.request.META["REMOTE_ADDR"]}' if hasattr(record, 'request') and 'REMOTE_ADDR' in record.request.META else 'IP: N/A'

        file_info = f'File: {record.pathname}, Line: {record.lineno}'

        custom_message = f'{user_info} - {record.levelname}: {record.getMessage()} - {file_info}'
        return custom_message

