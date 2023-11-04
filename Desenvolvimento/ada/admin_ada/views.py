from datetime import datetime
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.db import transaction
from django.urls import reverse
from area.models import Blockk
from attribution.models import TeacherQueuePosition
from attribution.views import schedule_attributtion_deadline_staff
from attribution_preference.models import Attribution_preference, Course_preference, Preference_schedule
from course.models import Course
from staff.models import Deadline
from timetable.models import Timetable, Timetable_user
from django.contrib.auth.decorators import login_required
# gource
from user.models import Proficiency, User

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
            if Deadline.objects.filter(year=year).exists():
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
    counter = 0
    for user in User.objects.all():
        counter += 1
        print(f'Proficiência {counter}/{User.objects.all().count()}', end='\r')
        blockks = user.blocks.all()
        for blockk in blockks:
            for course in Course.objects.filter(blockk=blockk):
                Proficiency.objects.get_or_create(
                    user=user,
                    is_competent=True,
                    course=course
                )

    if data['overwrite'] == 'true':
        Timetable_user.objects.filter(year=data['year']).update(user=None)
    else:
        for timetable in Timetable.objects.all():
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
       

        # fpa = Attribution_preference.objects.filter(year=data['year'])

        if Course_preference.objects.filter(blockk=blockk_obj, attribution_preference__year=data['year']).exists():
            print('Atribuição iniciada')
            schedule_attributtion_deadline_staff(data['startAssignmentDeadline'], 'startAssignmentDeadline', blockk_obj.registration_block_id, blockk_obj.registration_block_id) 
        else:
            print('Atribuição recusa por falta de preferências')


