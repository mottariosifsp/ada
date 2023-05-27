from datetime import date, datetime
from django.db import transaction
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from .models import Deadline

def is_staff(user):
    return user.is_staff

@user_passes_test(is_staff)
def attributionConfiguration(request):
    return render(request, 'configuration/attributionConfiguration.html') # apagar depois
    

def confirmConfiguration(request):
    if request.method == 'POST':
        
        startFPADeadline = datetime.strptime(request.POST.get('startFPADeadline'), '%Y-%m-%dT%H:%M')
        endFPADeadline = datetime.strptime(request.POST.get('endFPADeadline'), '%Y-%m-%dT%H:%M')
        startAssignmentDeadline = datetime.strptime(request.POST.get('startAssignmentDeadline'), '%Y-%m-%dT%H:%M')
        endAssignmentDeadline = datetime.strptime(request.POST.get('endAssignmentDeadline'), '%Y-%m-%dT%H:%M')
        startExchangeDeadline = datetime.strptime(request.POST.get('startExchangeDeadline'), '%Y-%m-%dT%H:%M')
        endExchangeDeadline = datetime.strptime(request.POST.get('endExchangeDeadline'), '%Y-%m-%dT%H:%M')

        # print(startFPADeadline)
        print(startFPADeadline)

        data = {
            'startFPADeadline': startFPADeadline,
            'endFPADeadline': endFPADeadline,
            'startAssignmentDeadline': startAssignmentDeadline,
            'endAssignmentDeadline': endAssignmentDeadline,
            'startExchangeDeadline': startExchangeDeadline,
            'endExchangeDeadline': endExchangeDeadline
        }

        saveDeadlines(data)

    return render(request, 'configuration/confirmConfiguration.html', data)

@transaction.atomic
def saveDeadlines(data):
    Deadline.objects.all().delete()
    Deadline.objects.create(
        name="startFPADeadline", 
        deadline_start=data['startFPADeadline'], 
        deadline_end=data['endFPADeadline'],
        )
    Deadline.objects.create(
        name="startAssignmentDeadline",
        deadline_start=data['startAssignmentDeadline'],
        deadline_end=data['endAssignmentDeadline'],
        )
    Deadline.objects.create(
        name="startExchangeDeadline",
        deadline_start=data['startExchangeDeadline'],
        deadline_end=data['endExchangeDeadline'],
        )