from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

def is_not_staff(user):
    return not user.is_staff

@user_passes_test(is_not_staff)
def home(request):
    return render(request, 'professor/home.html')
