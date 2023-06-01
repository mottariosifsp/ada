from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required

def is_not_staff(user):
    return not user.is_staff

@login_required(login_url='/user/login/')
@user_passes_test(is_not_staff)
def home(request):
    return render(request, 'professor/home_professor.html')
