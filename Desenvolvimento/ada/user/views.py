from multiprocessing import AuthenticationError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, render
from user.models import User
from django.contrib.auth import logout

def login(request):
    if request.method == 'POST':
        form = AuthenticationError(request, data=request.POST)
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

@login_required
def home(request):
    if request.user.is_staff:
        return redirect('home_staff')
    else:
        return redirect('home_professor')

def signup(request):
    return render(request, 'registration/signup.html')

def logout_view(request):
    logout(request)
    return redirect('login')