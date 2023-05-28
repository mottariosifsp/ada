from multiprocessing import AuthenticationError
from django.contrib.auth.decorators import login_required
from .models import User
from django.shortcuts import render, redirect
import re

def login(request):
    if request.method == 'POST':
        form = AuthenticationError(request, data=request.POST)
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

@login_required
def home(request):
    return render(request, "home.html")

def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        registration_id = request.POST.get('registration_id')

        if email and registration_id and password:
            if re.match(r'^[\w\.-]+@aluno\.ifsp\.edu\.br$', email):
                user = User.objects.create_user(email=email, registration_id=registration_id, password=password)
                user.save()
                return redirect('login')
            else:
                error_message = 'O e-mail deve ser do domínio @aluno.ifsp.edu.br'
                return render(request, 'registration/signup.html', {'error_message': error_message})
        else:
            return render(request, 'registration/signup.html')

    return render(request, 'registration/signup.html')