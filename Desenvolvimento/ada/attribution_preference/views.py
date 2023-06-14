from django.shortcuts import render
from .models import Attribution_preference, Preference_schedule, Course_preference, Attribution_preference_course_preference
from course.models import Course
from timetable.models import Timetable, Timeslot
from user.models import User, Job
from area.models import Area, Blockk
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

    timetables = Timetable.objects.filter(course__blockk__in=user_blocks)
    timetables = list(
        Timetable.objects.values_list('day_combo__day', 'classs', 'course', 'day_combo__timeslots__position')
    )

    # Converte para um objeto json
    converted_timetables = []
    for timetable in timetables:
        converted_timetable = {
            "day": timetable[0],
            "classs": timetable[1],
            "course": timetable[2],
            "timeslot_position": timetable[3]
        }
        converted_timetables.append(converted_timetable)

    json_data = json.dumps(converted_timetables)
    print(json_data)

    data = {
        'turno': turno,
        'user_blocks': user_blocks,
        'timetables': json_data
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
        user = request.user
        user_regime = user.job
        timetable = Timetable.objects.all()
        courses = Course.objects.all()

        areas = Area.objects.filter(blocks__in=user.blocks.all()).distinct()
        blocks = Blockk.objects.filter(areas__in=areas)

        user_area = []
        user_blocks = []

        for area in areas:
            area_obj = {
                'id': area.registrarion_area_id,
                'name_area': area.name_area,
                'acronym': area.acronym,
                'blocks': [block.acronym for block in area.blocks.all()]
            }
            user_area.append(area_obj)

        for block in blocks:
            block_obj = {
                'id': block.registration_block_id,
                'name_block': block.name_block,
                'acronym': block.acronym
            }
            user_blocks.append(block_obj)

        timetable_array = []

        for timetable_object in timetable:
            timetable_item = {
                'day': timetable_object.day,
                'hour_start': timetable_object.timeslot.hour_start.strftime('%H:%M:%S'),
                'course_acronym': timetable_object.course.acronym,
                'classs': timetable_object.classs.registration_class_id,
            }

            timetable_array.append(timetable_item)

        courses_array = []

        for course_object in courses:
            course_item = {
                'id': course_object.registration_course_id,
                'name': course_object.name_course,
                'acronym': course_object.acronym,
                'area': course_object.area.registration_area_id,
                'block': course_object.blockk.registration_block_id
            }
            courses_array.append(course_item)

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

        user_timeslot_hour = []
        user_timeslot_traceback = []
        user_preference_schedules = Preference_schedule.objects.filter(attribution_preference__user=request.user)
        for schedule in user_preference_schedules:
            begin = (schedule.timeslot.hour_start)            

            turno_sessao = None
            turno_posicao = None

            if begin >= datetime.time(7, 0, 0) and begin <= datetime.time(12, 0, 0):
                turno_sessao = 'mat'
                turno_posicao = next((i for i, slot in enumerate(turno['matutino']) if slot.hour_start == begin), None)
            elif begin >= datetime.time(13, 0, 0) and begin < datetime.time(18, 0, 0):
                turno_sessao = 'ves'
                turno_posicao = next((i for i, slot in enumerate(turno['vespertino']) if slot.hour_start == begin), None)
            elif begin >= datetime.time(18, 0, 0) and begin <= datetime.time(23, 0, 0):
                turno_sessao = 'not'
                turno_posicao = next((i for i, slot in enumerate(turno['noturno']) if slot.hour_start == begin), None)

            if turno_posicao is not None:
                turno_posicao += 1

            if schedule.day == 'monday':
                day = 'mon'
            elif schedule.day == 'tuesday':
                day = 'tue'
            elif schedule.day == 'wednesday':
                day = 'wed'
            elif schedule.day == 'thursday':
                day = 'thu'
            elif schedule.day == 'friday':
                day = 'fri'
            else:
                day = 'sat'

            string = {
                'frase': f'{day}-{turno_sessao}-{turno_posicao}',
                'posicao': turno_posicao,
                'sessao': turno_sessao,
                'dia': day,
                'hour': begin,
            } 
            user_timeslot_traceback.append(string)

        print(user_timeslot_traceback)
        print(user_blocks)
        print(user_area)
        print(timetable_array)

        data = {
            'work_regime': user_regime,
            'turno': turno,
            'user_disponibility': user_timeslot_traceback,
            'user_blocks': user_blocks,
            'user_areas': user_area,
            'timetables': timetable_array,
            'courses': courses_array
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

        return render(request, 'attribution_preference/confirm_attribution_preference.html')
    elif request.method == 'GET':
        data = {
            'preferred_courses': "baata"
        }

        return render(request, 'attribution_preference/confirm_attribution_preference.html', data)
