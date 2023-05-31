from multiprocessing import AuthenticationError
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

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
    return render(request, 'registration/signup.html')