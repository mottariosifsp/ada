from django.shortcuts import render
from .models import Attribution_preference, Preference_schedule, Course_preference, Attribution_preference_course_preference
from course.models import Course
from timetable.models import Timetable, Timeslot
from user.models import User, Job
from area.models import Area
from enums import enum
import json
import re
import datetime, time
from django.db import transaction

from django.utils.decorators import method_decorator

def attribution_preference(request):
    user = request.user
    user_blocks = user.blocks.all()

    turno = {
        'matutino': [],
        'matutinoAulas': 0,
        'vespertino': [],
        'vespertinoAulas': 0,
        'noturno': [],
        'noturnoAulas': 0
    }
        
    for timeslot in Timeslot.objects.all():
        if timeslot.hour_start >= datetime.time(7, 0, 0) and timeslot.hour_end <= datetime.time(12, 0, 0):
            turno['matutino'].append(timeslot)
        elif timeslot.hour_start >= datetime.time(13, 0, 0) and timeslot.hour_end <= datetime.time(18, 0, 0):
            turno['vespertino'].append(timeslot)
        elif timeslot.hour_start >= datetime.time(18, 0, 0) and timeslot.hour_end <= datetime.time(23, 0, 0):
            turno['noturno'].append(timeslot)
        
        turno['matutinoAulas'] = len(turno['matutino']) + 1
        turno['vespertinoAulas'] = len(turno['vespertino']) + 1
        turno['noturnoAulas'] = len(turno['noturno']) + 1

    data = {
        'turno': turno,
        'user_blocks': user_blocks
    }

    return render(request, 'attribution_preference/attribution_preference.html', data)

def convert_string_to_datetime(hora_string):
    pattern = r'(\d{1,2})(:\d{2})?\s*(a\.m\.|p\.m\.)'
    match = re.match(pattern, hora_string, re.IGNORECASE)

    if match:
        hour = int(match.group(1))
        minute = 0
        if match.group(2):
            minute = int(match.group(2)[1:])
        indicator = match.group(3).lower()

        if indicator == 'p.m.' and hour != 12:
            hour += 12
        elif indicator == 'a.m.' and hour == 12:
            hour = 0

        return datetime.time(hour=hour, minute=minute, second=0)

def courses_attribution_preference(request):
    work_regime = request.POST.get('work_regime')
    work_timeslots = request.POST.getlist('work_timeslots')
    json_data = [json.loads(item) for item in work_timeslots]

    timeslots = []

    for obj in json_data:
        for item in obj:
            hora_comeco = convert_string_to_datetime(item["hora_comeco"])
            dia_semana = item["dia_semana"]

            timeslot_preference = {
                "hora_comeco": hora_comeco,
                "dia_semana": dia_semana
            }

            timeslots.append(timeslot_preference)

    if request.method == 'POST':
        save_disponiility_preference(timeslots, work_regime, request.user)

        return render(request, 'attribution_preference/courses_attribution_preference.html')
    else:
        user_blocks = request.user.blocks.all()

        turno = {
            'matutino': [],
            'matutinoAulas': 0,
            'vespertino': [],
            'vespertinoAulas': 0,
            'noturno': [],
            'noturnoAulas': 0
        }
            
        for timeslot in Timeslot.objects.all():
            if timeslot.hour_start >= datetime.time(7, 0, 0) and timeslot.hour_end <= datetime.time(12, 0, 0):
                turno['matutino'].append(timeslot)
            elif timeslot.hour_start >= datetime.time(13, 0, 0) and timeslot.hour_end <= datetime.time(18, 0, 0):
                turno['vespertino'].append(timeslot)
            elif timeslot.hour_start >= datetime.time(18, 0, 0) and timeslot.hour_end <= datetime.time(23, 0, 0):
                turno['noturno'].append(timeslot)
            
            turno['matutinoAulas'] = len(turno['matutino']) + 1
            turno['vespertinoAulas'] = len(turno['vespertino']) + 1
            turno['noturnoAulas'] = len(turno['noturno']) + 1

        data = {
            'turno': turno,
            'user_blocks': user_blocks
        }

        return render(request, 'attribution_preference/courses_attribution_preference.html', data)


@transaction.atomic
def save_disponiility_preference(work_timeslots, work_regime, user):
    if user.job:
        user.job.delete()

    job = Job.objects.create(name_job=work_regime)
    user.job = job
    user.save()

    if not Attribution_preference.objects.filter(user=user).exists():
        Attribution_preference.objects.create(user=user)

    if Preference_schedule.objects.filter(attribution_preference__user=user).exists():
        Preference_schedule.objects.filter(attribution_preference__user=user).exists().delete()

    print(work_timeslots)

    for timeslot in work_timeslots:
        hora_comeco = timeslot["hora_comeco"]
        dia_semana = timeslot["dia_semana"]

        timeslot_object = Timeslot.objects.filter(hour_start=hora_comeco).first()
            
        if dia_semana == 'mon':
            day_object = enum.Day.monday.name
        elif dia_semana == 'tue':
            day_object = enum.Day.tuesday.name
        elif dia_semana == 'wed':
            day_object = enum.Day.wednesday.name
        elif dia_semana == 'thu':
            day_object = enum.Day.thursday.name
        elif dia_semana == 'fri':
            day_object = enum.Day.friday.name
        else:
            day_object = enum.Day.saturday.name
        
        Preference_schedule.objects.create(
            attribution_preference=Attribution_preference.objects.filter(user=user).first(),
            timeslot=timeslot_object,
            day=day_object
        )


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
