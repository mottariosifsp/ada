from django.shortcuts import render

from .models import Attribution_preference, Preference_schedule, Course_preference
from course.models import Course
from timetable.models import Timetable, Timeslot
from user.models import User, Job
from area.models import Area, Blockk
from staff.models import Deadline
from enums import enum
import json
import math
import re
import datetime, time
from django.db import transaction

from django.utils.decorators import method_decorator

def attribution_preference(request):
    user = request.user
    user_blocks = user.blocks.all()
    stage_fpas = []
    started_times = finished_times =  not_configured_times = configured_times = 0

    for blockk in user_blocks:
        status = ''
        start_day = ''
        start_time = ''
        end_day = ''
        end_time = ''
        if Deadline.objects.filter(blockk=blockk, name='STARTFPADEADLINE').exists():
            attribution_deadline = Deadline.objects.get(blockk=blockk, name='STARTFPADEADLINE')        
            now = datetime.datetime.today()
            if now > attribution_deadline.deadline_start and now < attribution_deadline.deadline_end:
                start_day = attribution_deadline.deadline_start.strftime("%d/%m/%Y")
                start_time = attribution_deadline.deadline_start.strftime("%H:%M:%S")
                end_day = attribution_deadline.deadline_end.strftime("%d/%m/%Y")
                end_time = attribution_deadline.deadline_end.strftime("%H:%M:%S")
                status = 'started'
                started_times += 1
            elif now < attribution_deadline.deadline_start:            
                start_day = attribution_deadline.deadline_start.strftime("%d/%m/%Y")
                start_time = attribution_deadline.deadline_start.strftime("%H:%M:%S")
                status = 'configured'
                configured_times += 1
            else:
                end_day = attribution_deadline.deadline_end.strftime("%d/%m/%Y")
                end_time = attribution_deadline.deadline_end.strftime("%H:%M:%S")
                status = 'finished'
                finished_times += 1
        else:
            status = 'not_configured'
            not_configured_times += 1

        blockk_stage_fpa = {
            'blockk': blockk,
            'status': status,
            'start_day': start_day,
            'start_time': start_time,
            'end_day': end_day,
            'end_time': end_time,
        }
        stage_fpas.append(blockk_stage_fpa)

    disponilibity_done = 'False'
    if Attribution_preference.objects.filter(user=user).exists():
        disponilibity_done = 'True'

    data = {
        'stage_fpas': stage_fpas,
        'started_times': started_times,
        'finished_times': finished_times,
        'not_configured_times': not_configured_times,
        'configured_times': configured_times,
        'is_pair': len(stage_fpas) % 2 == 0,
        'disponilibity_done': disponilibity_done
    }

    print(data)
    
    return render(request, 'attribution_preference/attribution_preference.html', data)


def disponibility_attribution_preference(request):
    user = request.user
    user_blocks = user.blocks.all()

    shift = {
        'morning': [],
        'morning_classes': 0,
        'afternoon': [],
        'afternoon_classes': 0,
        'nocturnal': [],
        'nocturnal_classes': 0
    }

    for timeslot in Timeslot.objects.all():
        if timeslot.hour_start >= datetime.time(7, 0, 0) and timeslot.hour_end <= datetime.time(12, 0, 0):
            shift['morning'].append(timeslot)
        elif timeslot.hour_start >= datetime.time(13, 0, 0) and timeslot.hour_end <= datetime.time(18, 0, 0):
            shift['afternoon'].append(timeslot)
        elif timeslot.hour_start >= datetime.time(18, 0, 0) and timeslot.hour_end <= datetime.time(23, 0, 0):
            shift['nocturnal'].append(timeslot)

        shift['morning_classes'] = len(shift['morning']) + 1
        shift['afternoon_classes'] = len(shift['afternoon']) + 1
        shift['nocturnal_classes'] = len(shift['nocturnal']) + 1

    timetables = Timetable.objects.filter(course__blockk__in=user_blocks)
    timetables = list(
        Timetable.objects.values_list('day_combo__day', 'classs', 'course', 'day_combo__timeslots__position')
    )

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

    timeslot = Timeslot.objects.get(id=1)

    start_minutes = timeslot.hour_start.hour * 60 + timeslot.hour_start.minute
    end_minutes = timeslot.hour_end.hour * 60 + timeslot.hour_end.minute
    variation = end_minutes - start_minutes
    max_quantity_cells = math.floor(480 / variation)
    quantity_cells_3_hours = math.floor(180 / variation)

    data = {
        'shift': shift,
        'timetables': json_data,
        'variation_minutes': variation, # alterar
        'max_quantity_cells': max_quantity_cells,
        'quantity_cells_3_hours': quantity_cells_3_hours
    }

    return render(request, 'attribution_preference/disponibility_attribution_preference.html', data)

def courses_attribution_preference(request):
    user_regime = request.POST.get('user_regime')
    user_timeslots = request.POST.getlist('user_timeslots')
    json_data = [json.loads(item) for item in user_timeslots]

    timeslots = []

    for obj in json_data:
        for item in obj:
            timeslot_begin_hour = convert_string_to_datetime(item["timeslot_begin_hour"])
            day_of_week = item["day_of_week"]

            timeslot_preference = {
                "timeslot_begin_hour": timeslot_begin_hour,
                "day_of_week": day_of_week
            }

            timeslots.append(timeslot_preference)

    if request.method == 'POST':
        save_disponiility_preference(timeslots, user_regime, request.user)

        return render(request, 'attribution_preference/courses_attribution_preference.html')
    else:
        user = request.user

        user_regime = user.job
        courses = Course.objects.all()
        
        user_area = []
        for area in Area.objects.filter(blocks__in=user.blocks.all().distinct()).distinct():
            area_obj = {
                'id': area.registration_area_id,
                'name': area.name_area,
                'acronym': area.acronym,
                'blocks': [block.registration_block_id for block in area.blocks.all()]
            }
            user_area.append(area_obj)
    
        user_block = []
        for block in user.blocks.all().distinct():
            block_obj = {
                'id': block.registration_block_id,
                'name': block.name_block,
                'acronym': block.acronym
            }
            user_block.append(block_obj)

        user_timetable = []
        for timetable_object in Timetable.objects.all():
            day_combo_objects = timetable_object.day_combo.all()
            day_combo_data = []

            for day_combo in day_combo_objects:
                day = day_combo.day
                timeslots = day_combo.timeslots.all()
                timeslot_data = []

                for timeslot in timeslots:
                    timeslot_data.append({
                        'timeslot_begin_hour': timeslot.hour_start.strftime('%H:%M:%S'),
                        'timeslot_end_hour': timeslot.hour_end.strftime('%H:%M:%S'),
                    })

                day_combo_data.append({
                    'day': day,
                    'timeslots': timeslot_data,
                })

            timetable_item = {
                'id': timetable_object.id,
                'day_combo': day_combo_data,
                'course_acronym': timetable_object.course.acronym,
                'course_name': timetable_object.course.name_course,
                'course_id': timetable_object.course.registration_course_id,
                'classs': timetable_object.classs.registration_class_id,
            }

            user_timetable.append(timetable_item)

        user_courses = []
        for course_object in Course.objects.all():
            course_item = {
                'id': course_object.registration_course_id,
                'name': course_object.name_course,
                'acronym': course_object.acronym,
                'area': course_object.area.registration_area_id,
                'block': course_object.blockk.registration_block_id
            }
            user_courses.append(course_item)

        shift = {
            'morning': [],
            'morning_classes': 0,
            'afternoon': [],
            'afternoon_classes': 0,
            'nocturnal': [],
            'nocturnal_classes': 0
        }

        for timeslot in Timeslot.objects.all():
            if timeslot.hour_start >= datetime.time(7, 0, 0) and timeslot.hour_end <= datetime.time(12, 0, 0):
                shift['morning'].append(timeslot)
            elif timeslot.hour_start >= datetime.time(13, 0, 0) and timeslot.hour_end <= datetime.time(18, 0, 0):
                shift['afternoon'].append(timeslot)
            elif timeslot.hour_start >= datetime.time(18, 0, 0) and timeslot.hour_end <= datetime.time(23, 0, 0):
                shift['nocturnal'].append(timeslot)

            shift['morning_classes'] = len(shift['morning']) + 1
            shift['afternoon_classes'] = len(shift['afternoon']) + 1
            shift['nocturnal_classes'] = len(shift['nocturnal']) + 1

        user_timeslot_table = []
        user_preference_schedules = Preference_schedule.objects.filter(attribution_preference__user=request.user)
        for schedule in user_preference_schedules:
            timeslot_begin_hour = (schedule.timeslot.hour_start)

            shift_type = None
            shift_position = None

            if timeslot_begin_hour >= datetime.time(7, 0, 0) and timeslot_begin_hour <= datetime.time(12, 0, 0):
                shift_type = 'mor'
                shift_position = next((i for i, slot in enumerate(shift['morning']) if slot.hour_start == timeslot_begin_hour), None)
            elif timeslot_begin_hour >= datetime.time(13, 0, 0) and timeslot_begin_hour < datetime.time(18, 0, 0):
                shift_type = 'aft'
                shift_position = next((i for i, slot in enumerate(shift['afternoon']) if slot.hour_start == timeslot_begin_hour),
                                     None)
            elif timeslot_begin_hour >= datetime.time(18, 0, 0) and timeslot_begin_hour <= datetime.time(23, 0, 0):
                shift_type = 'noc'
                shift_position = next((i for i, slot in enumerate(shift['nocturnal']) if slot.hour_start == timeslot_begin_hour), None)

            if shift_position is not None:
                shift_position += 1

            if schedule.day == 'monday':
                shift_day = 'mon'
            elif schedule.day == 'tuesday':
                shift_day = 'tue'
            elif schedule.day == 'wednesday':
                shift_day = 'wed'
            elif schedule.day == 'thursday':
                shift_day = 'thu'
            elif schedule.day == 'friday':
                shift_day = 'fri'
            else:
                shift_day = 'sat'

            string = {
                'id': f'{shift_day}-{shift_type}-{shift_position}',
                'position': shift_position,
                'type': shift_type,
                'day': shift_day,
                'timeslot_begin_hour': timeslot_begin_hour.strftime('%H:%M:%S'),
            }
            user_timeslot_table.append(string)
        
        if user_regime.name_job == "rde":
            user_regime_choosed = user_regime
            user_regime_choosed.name_job = '40'
        else:
            user_regime_choosed = user_regime

        data = {
            'user_regime': user_regime_choosed,
            'shift': shift,
            'user_disponibility': user_timeslot_table,
            'user_blocks': user_block,
            'user_areas': user_area,
            'user_timetables': user_timetable,
            'user_courses': user_courses
        }

        return render(request, 'attribution_preference/courses_attribution_preference.html', data)

def show_attribution_preference(request):
    work_courses = request.POST.getlist('timetable')
    timetable = []

    for item in work_courses:
        item_dict = json.loads(item)

        timetable.append(item_dict)

    if request.method == 'POST':
        save_courses_preference(timetable, request.user)

        return render(request, 'attribution_preference/attribution_preference.html')
    elif request.method == 'GET':
        user = request.user
        
        if user.job is None:
            user_regime = " "
        else:
            user_regime = user.job.name_job

        shift = {
            'morning': [],
            'morning_classes': 0,
            'afternoon': [],
            'afternoon_classes': 0,
            'nocturnal': [],
            'nocturnal_classes': 0
        }

        for timeslot in Timeslot.objects.all():
            if timeslot.hour_start >= datetime.time(7, 0, 0) and timeslot.hour_end <= datetime.time(12, 0, 0):
                shift['morning'].append(timeslot)
            elif timeslot.hour_start >= datetime.time(13, 0, 0) and timeslot.hour_end <= datetime.time(18, 0, 0):
                shift['afternoon'].append(timeslot)
            elif timeslot.hour_start >= datetime.time(18, 0, 0) and timeslot.hour_end <= datetime.time(23, 0, 0):
                shift['nocturnal'].append(timeslot)

            shift['morning_classes'] = len(shift['morning']) + 1
            shift['afternoon_classes'] = len(shift['afternoon']) + 1
            shift['nocturnal_classes'] = len(shift['nocturnal']) + 1

        user_timeslot_traceback = []
        user_preference_schedules = Preference_schedule.objects.filter(attribution_preference__user=request.user)
        for schedule in user_preference_schedules:
            begin = (schedule.timeslot.hour_start)

            shift_type = None
            shift_position = None

            if begin >= datetime.time(7, 0, 0) and begin <= datetime.time(12, 0, 0):
                shift_type = 'mor'
                shift_position = next((i for i, slot in enumerate(shift['morning']) if slot.hour_start == begin), None)
            elif begin >= datetime.time(13, 0, 0) and begin < datetime.time(18, 0, 0):
                shift_type = 'aft'
                shift_position = next((i for i, slot in enumerate(shift['afternoon']) if slot.hour_start == begin),
                                     None)
            elif begin >= datetime.time(18, 0, 0) and begin <= datetime.time(23, 0, 0):
                shift_type = 'noc'
                shift_position = next((i for i, slot in enumerate(shift['nocturnal']) if slot.hour_start == begin), None)

            if shift_position is not None:
                shift_position += 1

            if schedule.day == 'monday':
                day_of_week = 'mon'
            elif schedule.day == 'tuesday':
                day_of_week = 'tue'
            elif schedule.day == 'wednesday':
                day_of_week = 'wed'
            elif schedule.day == 'thursday':
                day_of_week = 'thu'
            elif schedule.day == 'friday':
                day_of_week = 'fri'
            else:
                day_of_week = 'sat'

            string = {
                'id': f'{day_of_week}-{shift_type}-{shift_position}'
            }
            user_timeslot_traceback.append(string)

        user_courses_traceback = []
        user_courses = Course_preference.objects.filter(attribution_preference__user=request.user)
        for preference in user_courses:

            shift_period = ''
            day_combo = preference.timetable.day_combo.first()
            if day_combo:
                first_timeslot = day_combo.timeslots.first()
                if first_timeslot:
                    if first_timeslot.hour_start >= datetime.time(7, 0, 0) and first_timeslot.hour_end <= datetime.time(12, 0, 0):
                        shift_period = 'morning'
                    elif first_timeslot.hour_start >= datetime.time(13, 0, 0) and first_timeslot.hour_end <= datetime.time(18, 0, 0):
                        shift_period = 'afternoon'
                    elif first_timeslot.hour_start >= datetime.time(18, 0, 0) and first_timeslot.hour_end <= datetime.time(23, 0, 0):
                        shift_period = 'nocturnal'

            timetable_object = {
                'acronym': preference.timetable.course.acronym,
                'name_course': preference.timetable.course.name_course,
                'course_area': preference.timetable.course.area.name_area,
                'period': shift_period,
                'classes': day_combo.timeslots.count(), 
            }
            user_courses_traceback.append(timetable_object)

        if user_regime and user_timeslot_traceback and user_courses:
            is_fpa_done = True
        else:
            is_fpa_done = False

        data = {
            'is_fpa_done': is_fpa_done,
            'shift': shift,
            'user_regime': user_regime,
            'user_disponibility_choosed': user_timeslot_traceback,
            'user_courses_choosed': user_courses_traceback,
        }

        return render(request, 'attribution_preference/show_attribution_preference.html', data)

@transaction.atomic
def save_disponiility_preference(user_timeslots, user_regime, user):
    job = Job.objects.create(name_job=user_regime)
    user.job = None
    user.job = job
    user.save()

    if not Attribution_preference.objects.filter(user=user).exists():
        Attribution_preference.objects.create(user=user)

    if Preference_schedule.objects.filter(attribution_preference__user=user).exists():
        Preference_schedule.objects.filter(attribution_preference__user=user).delete()

    for timeslot in user_timeslots:
        timeslot_begin_hour = timeslot["timeslot_begin_hour"]
        day_of_week = timeslot["day_of_week"]

        timeslot_object = Timeslot.objects.filter(hour_start=timeslot_begin_hour).first()

        if day_of_week == 'mon':
            day_object = enum.Day.monday.name
        elif day_of_week == 'tue':
            day_object = enum.Day.tuesday.name
        elif day_of_week == 'wed':
            day_object = enum.Day.wednesday.name
        elif day_of_week == 'thu':
            day_object = enum.Day.thursday.name
        elif day_of_week == 'fri':
            day_object = enum.Day.friday.name
        else:
            day_object = enum.Day.saturday.name

        Preference_schedule.objects.create(
            attribution_preference=Attribution_preference.objects.filter(user=user).first(),
            timeslot=timeslot_object,
            day=day_object
        )


@transaction.atomic
def save_courses_preference(work_courses, user):
    if Course_preference.objects.filter(attribution_preference__user=user).exists():
        Course_preference.objects.filter(attribution_preference__user=user).delete()

    for courses in work_courses:
        for i, course in enumerate(courses, 1):
            id_timetable = int(course['id_timetable'])
            timetable = Timetable.objects.filter(id=id_timetable).first()

            Course_preference.objects.create(
                attribution_preference=Attribution_preference.objects.filter(user=user).first(),
                timetable=timetable
            )

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

