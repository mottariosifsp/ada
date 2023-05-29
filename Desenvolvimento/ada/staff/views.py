from datetime import datetime
from django.db import transaction
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from .models import Deadline
from user.models import User
from django.utils import timezone

def is_staff(user):
    return user.is_staff

# prazos

@user_passes_test(is_staff)
def home(request):
    return render(request, 'staff/home.html')


@user_passes_test(is_staff)
def deadline_configuration(request):

    user_blocks = request.user.blocks.all()
    
    data = {
        'user_blocks': user_blocks
    }

    return render(request, 'staff/deadline/deadline_configuration.html', data)
    

def confirm_deadline_configuration(request):
    if request.method == 'POST':
        
        startFPADeadline = datetime.strptime(request.POST.get('startFPADeadline'), '%Y-%m-%dT%H:%M')
        endFPADeadline = datetime.strptime(request.POST.get('endFPADeadline'), '%Y-%m-%dT%H:%M')
        startAssignmentDeadline = datetime.strptime(request.POST.get('startAssignmentDeadline'), '%Y-%m-%dT%H:%M')
        endAssignmentDeadline = datetime.strptime(request.POST.get('endAssignmentDeadline'), '%Y-%m-%dT%H:%M')
        startExchangeDeadline = datetime.strptime(request.POST.get('startExchangeDeadline'), '%Y-%m-%dT%H:%M')
        endExchangeDeadline = datetime.strptime(request.POST.get('endExchangeDeadline'), '%Y-%m-%dT%H:%M')

        print(startFPADeadline)

        data = {
            'startFPADeadline': startFPADeadline,
            'endFPADeadline': endFPADeadline,
            'startAssignmentDeadline': startAssignmentDeadline,
            'endAssignmentDeadline': endAssignmentDeadline,
            'startExchangeDeadline': startExchangeDeadline,
            'endExchangeDeadline': endExchangeDeadline,
            'user_block': request.user.blocks.all()
        }

        save_deadline(data)

    return render(request, 'staff/deadline/confirm_deadline_configuration.html', data)

def show_current_deadline(request):
    deadlines = Deadline.objects.all()
    now = timezone.now() 

    if(deadlines.get(name="startFPADeadline").deadline_start <= now and deadlines.get(name="startFPADeadline").deadline_end >= now):
        actualDeadline = "FPA"
    elif(deadlines.get(name="startAssignmentDeadline").deadline_start <= now and deadlines.get(name="startAssignmentDeadline").deadline_end >= now):
        actualDeadline = "Assignment"
    elif(deadlines.get(name="startExchangeDeadline").deadline_start <= now and deadlines.get(name="startExchangeDeadline").deadline_end >= now):
        actualDeadline = "Exchange"
    else:
        actualDeadline = "none"

    data = {
        'actualDeadline': actualDeadline
    }

    return render(request, 'staff/deadline/show_current_deadline.html', data)

@transaction.atomic
def save_deadline(data):
    Deadline.objects.all().delete()
    Deadline.objects.create(
        name="startFPADeadline", 
        deadline_start=data['startFPADeadline'], 
        deadline_end=data['endFPADeadline'],
        blocks=data['userBlock'],
        )
    Deadline.objects.create(
        name="startAssignmentDeadline",
        deadline_start=data['startAssignmentDeadline'],
        deadline_end=data['endAssignmentDeadline'],
        blocks=data['userBlock'],
        )
    Deadline.objects.create(
        name="startExchangeDeadline",
        deadline_start=data['startExchangeDeadline'],
        deadline_end=data['endExchangeDeadline'],
        blocks=data['userBlock'],
        )

#professor views

@user_passes_test(is_staff)
def professors_list(request):
    professors = User.objects.filter(is_superuser=False)
    return render(request, 'staff/professors_list.html', {'professors': professors})
