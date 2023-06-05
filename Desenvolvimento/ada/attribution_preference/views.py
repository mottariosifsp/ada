from django.shortcuts import render
from .models import Attribution_preference, Preference_schedule, Course_preference, Attribution_preference_course_preference
from course.models import Course
from timetable.models import Timetable, Timeslot
import json
from django.db import transaction


def attribution_preference(request):
    course = Course.objects.all()
    turno = {
        'matu': [],
        'vesp': [],
        'notu': []
    }
    for i in range(1,7):
        turno['matu'].append(Timeslot.objects.filter(position=i))
        turno['vesp'].append(Timeslot.objects.filter(position=i+6))
        turno['notu'].append(Timeslot.objects.filter(position=i+12))

    print(turno)


    # timeslot.
    data = {
        'courses': course,
        'turno': turno
    }

    return render(request, 'attribution_preference/attribution_preference.html', data)

def confirm_attribution_preference(request):
    work_regime = request.POST.get('work_regime')

    if request.method == 'POST':
        data = {
            'work_regime': work_regime
        }
        print(data)
        # save_course_preference(preferred_courses, request)
        print("sim")

        return render(request, 'attribution_preference/confirm_attribution_preference.html')
    elif request.method == 'GET':
        data = {
            'preferred_courses': "baata"
        }
        print(data)

        return render(request, 'attribution_preference/confirm_attribution_preference.html', data)

#@transaction.atomic
#def save_course_preference(preferred_courses, request):
#    for course in preferred_courses:
#        if Course_preference.objects.filter(attribution_preference_course_preference_attribution_preference_user=request.user).exists():
#            Course_preference.objects.filter(attribution_preference_course_preference_attribution_preference_user=request.user).delete() 
#            Course_preference.objects.create(
#            course=Course.objects.filter(name_course=course.nome), 
#            course_name=course.nome,
#            count_course=data[course.numAulas], 
#            priority=course.prioridade,
#            period=course.turno
#            )
#        else:
##            Course_preference.objects.create(
#            course=Course.objects.filter(name_course=course.nome), 
#            course_name=course.nome,
 #           count_course=data[course.numAulas], 
 #           priority=course.prioridade,
 #           period=course.turno
 #           )