from django.shortcuts import render
from .models import Attribution_preference, Preference_schedule, Course_preference,  Attribution_preference_course_preference
from course.models import Course
from django.db import transaction


def attributionPreference(request):
    courses = Course.objects.all()
    data = {
        'courses': courses,
    }

    return render(request, 'attribution_preference/attributionPreference.html', data)

def confirmAttributionPreference(request):
    work_regime = request.POST.get('work_regime')
    preferred_courses = request.POST.getlist('work_courses[]')

    if request.method == 'POST':
        data = {
            'work_regime': work_regime,
            'preferred_courses': preferred_courses
        }

        saveCoursePreference(preferred_courses)
        print("sim")

        return render(request, 'attribution_preference/confirmAttributionPreference.html')
    elif request.method == 'GET':        
        

        return render(request, 'attribution_preference/confirmAttributionPreference.html', data)

@transaction.atomic
def saveCoursePreference(preferred_courses):
    if Course_preference.objects.filter(attribution_preference_course_preference__attribution_preference__user=user).exists():
        Course_preference.objects.filter(attribution_preference_course_preference__attribution_preference__user=user).delete()
        for course in preferred_courses:
            Course_preference.objects.create(
                course=course.nome,
                count_course=course.numAulas,
                priority=course.turno,
                period=course.prioridade
            )
    else:
        for course in preferred_courses:
            Course_preference.objects.create(
                course=course.nome,
                count_course=course.numAulas,
                priority=course.turno,
                period=course.prioridade
            )

