from datetime import datetime
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.db import transaction
from django.urls import reverse
from area.models import Blockk
from attribution.views import schedule_attributtion_deadline_staff
from attribution_preference.models import Course_preference
from staff.models import Deadline
from timetable.models import Timetable, Timetable_user
from django.contrib.auth.decorators import login_required

@login_required
def deadline_configuration(request):
    
    return render(request, 'admin/deadline_configuration.html')

@login_required
def deadline_configuration_confirm(request):
    if request.method == 'POST':       
        print('POST')
        date_format = "%Y-%m-%dT%H:%M"
        year = request.POST.get('year')
        semester = request.POST.get('semester')
        year = str(year)+'.'+str(semester)
        startFPADeadline = datetime.strptime(request.POST.get('startFPADeadline'), date_format)
        endFPADeadline = datetime.strptime(request.POST.get('endFPADeadline'), date_format)
        startAssignmentDeadline = datetime.strptime(request.POST.get('startAssignmentDeadline'), date_format)
        endAssignmentDeadline = datetime.strptime(request.POST.get('endAssignmentDeadline'), date_format)
        overwrite = request.POST.get('overwrite')
        if overwrite == 'false':
            if year == Deadline.objects.all().first().year:
                return JsonResponse({'error': 'Já houve uma atribuição para esse semetre neste ano.'}, status=400)

        data = {
            'year': year,
            'startFPADeadline': startFPADeadline,
            'endFPADeadline': endFPADeadline,
            'startAssignmentDeadline': startAssignmentDeadline,
            'endAssignmentDeadline': endAssignmentDeadline,
            'overwrite': overwrite,
        }

        save_deadline(data) 

        return JsonResponse({'redirect':reverse(deadline_configuration_confirm)})
        # return render(request, 'admin/deadline_configuration_confirm.html', data)
    else:
        return render(request, 'admin/deadline_configuration_confirm.html')

@transaction.atomic
def save_deadline(data):
    if data['overwrite'] == 'true':
        Timetable_user.objects.filter(year=data['year']).update(user=None)
    else:
        print('oiers')
        for timetable in Timetable.objects.all():
            print(timetable)
            Timetable_user.objects.create(
                timetable=timetable,
                user=None,
                year=data['year'],
            )

    Deadline.objects.all().delete()   
    
    for blockk_obj in Blockk.objects.all():
        print(blockk_obj.name_block, end=': ')
        Deadline.objects.create(
            year=data['year'],
            name="STARTFPADEADLINE",
            deadline_start=data['startFPADeadline'],
            deadline_end=data['endFPADeadline'],
            blockk=blockk_obj,
        )
        Deadline.objects.create(
            year=data['year'],
            name="STARTASSIGNMENTDEADLINE",
            deadline_start=data['startAssignmentDeadline'],
            deadline_end=data['endAssignmentDeadline'],
            blockk=blockk_obj,
        )
        # if Course_preference.objects.filter(blockk=blockk_obj).exists():
        #     print('Atribuição iniciada')
        #     schedule_attributtion_deadline_staff(data['startAssignmentDeadline'], 'startAssignmentDeadline', blockk_obj.registration_block_id, blockk_obj.registration_block_id) 
        # else:
        #     print('Atribuição recusa por falta de preferências')