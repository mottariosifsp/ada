from django.shortcuts import render
from .models import Attribution_preference, Preference_schedule, Course_preference,  Attribution_preference_course_preference
from course.models import Course

# 
def attributionPreference(request):
    courses = Course.objects.all()
    data = {
        'courses': courses,
    }

    return render(request, 'attribution_preference/attributionPreference.html', data)

def confirmAttributionPreference(request):
    return render(request, 'attribution_preference/confirmAttributionPreference.html')