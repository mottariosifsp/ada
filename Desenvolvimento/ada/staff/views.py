from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

def is_staff(user):
    return user.is_staff

@user_passes_test(is_staff)
def home(request):
    return render(request, 'home.html')

@user_passes_test(is_staff)
def professors_list(request):
    return render(request, 'professors_list.html')


