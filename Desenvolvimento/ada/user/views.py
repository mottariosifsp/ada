from multiprocessing import AuthenticationError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import render
from user.models import User

def login(request):
    if request.method == 'POST':
        form = AuthenticationError(request, data=request.POST)
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

@login_required
def home(request):
    if request.user.is_staff:
        return render(request, "staff/home_staff.html")
    else:
        return render(request, "professor/home_professor.html")   

def signup(request):
    return render(request, 'registration/signup.html')