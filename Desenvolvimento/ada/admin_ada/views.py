from datetime import datetime
from django.shortcuts import render
from django.db import transaction
from area.models import Blockk
from attribution.views import schedule_attributtion_deadline_staff
from attribution_preference.models import Course_preference
from staff.models import Deadline
from timetable.models import Timetable_user

def deadline_configuration(request):
    return render(request, 'admin/deadline_configuration.html')


def deadline_configuration_confirm(request):
    if request.method == 'POST':       

        date_format = "%Y-%m-%dT%H:%M"

        startFPADeadline = datetime.strptime(request.POST.get('startFPADeadline'), date_format)
        endFPADeadline = datetime.strptime(request.POST.get('endFPADeadline'), date_format)
        startAssignmentDeadline = datetime.strptime(request.POST.get('startAssignmentDeadline'), date_format)
        endAssignmentDeadline = datetime.strptime(request.POST.get('endAssignmentDeadline'), date_format)

        print(startFPADeadline)

        data = {
            'startFPADeadline': startFPADeadline,
            'endFPADeadline': endFPADeadline,
            'startAssignmentDeadline': startAssignmentDeadline,
            'endAssignmentDeadline': endAssignmentDeadline,
        }
        for time in Timetable_user.objects.all():
            time.user = None
            time.save()

        save_deadline(data) 


        return render(request, 'admin/deadline_configuration_confirm.html', data)

@transaction.atomic

def save_deadline(data):

    Timetable_user.objects.all().update(user=None)


    Deadline.objects.all().delete()   
    
    for blockk_obj in Blockk.objects.all():
        print(blockk_obj.name_block, end=': ')
        Deadline.objects.create(
            name="STARTFPADEADLINE",
            deadline_start=data['startFPADeadline'],
            deadline_end=data['endFPADeadline'],
            blockk=blockk_obj,
        )
        Deadline.objects.create(
            name="STARTASSIGNMENTDEADLINE",
            deadline_start=data['startAssignmentDeadline'],
            deadline_end=data['endAssignmentDeadline'],
            blockk=blockk_obj,
        )
        if Course_preference.objects.filter(blockk=blockk_obj).exists():
            print('Atribuição iniciada')
            schedule_attributtion_deadline_staff(data['startAssignmentDeadline'], 'startAssignmentDeadline', blockk_obj.registration_block_id, blockk_obj.registration_block_id) 
        else:
            print('Atribuição recusa por falta de preferências')