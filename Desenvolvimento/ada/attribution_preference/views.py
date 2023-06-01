from django.shortcuts import render
from .models import Attribution_preference, Preference_schedule, Course_preference, Attribution_preference_course_preference
from course.models import Course
from timetable.models import Timetable, Timeslot
import json
from django.db import transaction


def attribution_preference(request):
    course = Course.objects.all()
    timeslot = Timeslot.objects.all()
    # timeslot.
    data = {
        'courses': course
    }

    return render(request, 'attribution_preference/attribution_preference.html', data)

def confirm_attribution_preference(request):
    work_regime = request.POST.get('work_regime')
    preferred_courses = request.POST.getlist('work_courses[]')

    if request.method == 'POST':
        data = {
            'work_regime': work_regime,
            'preferred_courses': preferred_courses
        }
        print(data)
        save_course_preference(preferred_courses, request)
        print("sim")

        return render(request, 'attribution_preference/confirm_attribution_preference.html')
    elif request.method == 'GET':
        courses = Course_preference.objects.all()
        data = {
            'preferred_courses': courses
        }
        print(data)

        return render(request, 'attribution_preference/confirm_attribution_preference.html', data)

@transaction.atomic
def save_course_preference(preferred_courses, request):
    for course in preferred_courses:
        if Course_preference.objects.filter(attribution_preference_course_preference_attribution_preference_user=request.user).exists():
            Course_preference.objects.filter(attribution_preference_course_preference_attribution_preference_user=request.user).delete() 
            Course_preference.objects.create(
            course=Course.objects.filter(name_course=course.nome), 
            course_name=course.nome,
            count_course=data[course.numAulas], 
            priority=course.prioridade,
            period=course.turno
            )
        else:
            Course_preference.objects.create(
            course=Course.objects.filter(name_course=course.nome), 
            course_name=course.nome,
            count_course=data[course.numAulas], 
            priority=course.prioridade,
            period=course.turno
            )