from django.shortcuts import render
from .models import Attribution_preference, Preference_schedule, Course_preference,  Attribution_preference_course_preference
from course.models import Course
import json
from django.db import transaction


def attributionPreference(request):
    courses = Course.objects.all()
    data = {
        'courses': courses,
    }

    return render(request, 'attribution_preference/attributionPreference.html', data)

def confirmAttributionPreference(request):
    work_regime = request.POST.get('work_regime')
    preferred_courses = request.POST.getlist('work_courses')

    if request.method == 'POST':
        data = {
            'work_regime': work_regime,
            'preferred_courses': preferred_courses
        }
        print(data)
        saveCoursePreference(preferred_courses, request)
        print("sim")

        return render(request, 'attribution_preference/confirmAttributionPreference.html')
    elif request.method == 'GET':
        courses = Course_preference.objects.all()
        data = {
            'preferred_courses': courses
        }
        print(data)

        return render(request, 'attribution_preference/confirmAttributionPreference.html', data)

@transaction.atomic
def saveCoursePreference(preferred_courses, request):
    if Course_preference.objects.filter(attribution_preference_course_preference__attribution_preference__user=request.user).exists():
        Course_preference.objects.filter(attribution_preference_course_preference__attribution_preference__user=request.user).delete()
        for course in preferred_courses:
            Course_preference.objects.create(
                course=course,
                count_course=course.numAulas,
                priority=course.turno,
                period=course.prioridade
            )
    else:
        for course in preferred_courses:
            Course_preference.objects.create(
                course=course,
                count_course=course.numAulas,
                priority=course.turno,
                period=course.prioridade
            )