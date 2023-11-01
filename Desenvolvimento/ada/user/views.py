# gource
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
from datetime import datetime
import re
from django import forms

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
    
def professor_authenticate(request, email, password):
    try:
        professor = User.objects.get(email=email)

        if professor.check_password(password):
            professor.is_active = True
            professor.save()

            return True
    except User.DoesNotExist:
        pass

    return False

def signup(request):
    class RegistrationForm(forms.Form):
        email = forms.EmailField(label='Email')
        password = forms.CharField(widget=forms.PasswordInput, label='Senha')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            if re.match(r'^[\w\.-]+@ifsp\.edu\.br$', email):

                if professor_authenticate(request, email, password):
                    return redirect('login')
                else:
                    error_message = 'E-mail ou senha incorreto(a)'
                    return render(request, 'registration/signup.html', {'form': form, 'error_message': error_message})
            else:
                error_message = 'O email deve ser do tipo @ifsp.edu.br'
                return render(request, 'registration/signup.html', {'form': form, 'error_message': error_message})
        else:
            error_message = 'Formulário inválido'
            return render(request, 'registration/signup.html', {'form': form, 'error_message': error_message})
    else:
        form = RegistrationForm()

    return render(request, 'registration/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def handler404(request, exception):
    custom_logger = logging.getLogger('custom_logger')

    user = request.user if hasattr(request, 'user') else None

    if user and user.is_authenticated:
        user_info = f'Nome do usuário User: {user.first_name}'
    else:
        user_info = f'IP: {request.META["REMOTE_ADDR"]}' if hasattr(request,
                                                                    'META') and 'REMOTE_ADDR' in request.META else 'IP: N/A'
    custom_logger.error("Erro 404 - %s - Página não encontrada: %s", user_info, request.path)

    return render(request, 'error/404.html', status=404)


def handler500(request):
    exc_type, exc_value, exc_traceback = sys.exc_info()

    custom_logger = logging.getLogger('custom_logger')
    user = request.user if hasattr(request, 'user') else None
    if user and user.is_authenticated:
        user_info = f'Nome do Usuário: {user.first_name}'
    else:
        user_info = f'IP: {request.META["REMOTE_ADDR"]}' if hasattr(request,
                                                                    'META') and 'REMOTE_ADDR' in request.META else 'IP: N/A'
    custom_logger.error("Erro 500 - %s - Tipo de Exceção: %s, Mensagem: %s - Erro na página: %s",
                        user_info,
                        exc_type.__name__,
                        str(exc_value), request.path)

    return render(request, 'error/500.html', status=500)

def provocar_erro_500(request):
    raise Exception("Erro 500 forçado - Internal Server Error")
