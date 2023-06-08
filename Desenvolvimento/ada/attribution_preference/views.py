from django.shortcuts import render
from .models import Attribution_preference, Preference_schedule, Course_preference, Attribution_preference_course_preference
from course.models import Course
from timetable.models import Timetable, Timeslot
from user.models import User
from area.models import Area
import json
import datetime
from django.db import transaction


def attribution_preference(request):
    course = Course.objects.all()
    user_blocks = request.user.blocks.all()
    user_areas = set()
    for block in user_blocks:
        areas = block.areas.all()
        user_areas.update(areas)

    timeslots = Timeslot.objects.filter(area__in=user_areas)

    grade = []

    for area in user_areas:
        turno = {
            'matutino': [],
            'matutinoAulas': 0,
            'vespertino': [],
            'vespertinoAulas': 0,
            'noturno': [],
            'noturnoAulas': 0
        }

        for timeslot in Timeslot.objects.filter(area=area):
            if timeslot.hour_start >= datetime.time(7, 0, 0) and timeslot.hour_end <= datetime.time(12, 0, 0):
                turno['matutino'].append(timeslot)
            elif timeslot.hour_start >= datetime.time(13, 0, 0) and timeslot.hour_end <= datetime.time(18, 0, 0):
                turno['vespertino'].append(timeslot)
            elif timeslot.hour_start >= datetime.time(18, 0, 0) and timeslot.hour_end <= datetime.time(23, 0, 0):
                turno['noturno'].append(timeslot)
        
        turno['matutinoAulas'] = len(turno['matutino']) + 1
        turno['vespertinoAulas'] = len(turno['vespertino']) + 1
        turno['noturnoAulas'] = len(turno['noturno']) + 1
        grade.append(turno);

    # print(turno)

    data = {
        'courses': course,
        'grade_turnos': grade,
        'areas': user_areas
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