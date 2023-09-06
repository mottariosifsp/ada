from django.urls import reverse
from django.http import JsonResponse
from area.models import Area, Blockk
from attribution.task import attribution_deadline_start, cancel_all_tasks, cancel_scheduled_task, get_time_left, schedule_task, schedule_deadline
from attribution_preference.views import convert_string_to_datetime, save_disponiility_preference
from classs.models import Classs
from course.models import Course
from enums.enum import Priority
from staff.models import Criteria, Deadline
from timetable.models import Timeslot, Timetable, Timetable_user
from user.models import Proficiency, User
from attribution.models import TeacherQueuePosition
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
import json
from django.db.models import F, Sum, Value  
from django.db import transaction
from django.utils import timezone
from datetime import datetime, timedelta, timezone
from django.core.mail import send_mail, EmailMessage
import xml.etree.ElementTree as ET
import os

from django.contrib.auth.decorators import login_required
from attribution_preference.models import Course_preference, Attribution_preference, Preference_schedule

from django.utils.decorators import method_decorator

from common.date_utils import day_to_number
@login_required
def attribution(request):
    
    # cancel_all_tasks()
    # for time in Timetable_user.objects.all():
    #     time.user = None
    #     time.save()

    blockk = Blockk.objects.get(registration_block_id=request.GET.get('blockk'))
    consider_deadline = True
    
    if request.method == 'GET':
        
        if consider_deadline:
            if Deadline.objects.filter(blockk=blockk, name='STARTASSIGNMENTDEADLINE').exists():
                attribution_deadline = Deadline.objects.get(blockk=blockk, name='STARTASSIGNMENTDEADLINE')        
                now = datetime.datetime.today()
                if now > attribution_deadline.deadline_end:

                    return render(request, 'attribution/attribution_error_page_after.html', {'blockk': request.GET.get('blockk')})
                elif now < attribution_deadline.deadline_start:            
                    day = attribution_deadline.deadline_start.strftime("%d/%m/%Y")
                    time = attribution_deadline.deadline_start.strftime("%H:%M:%S")

                    data = {
                        'day': day,
                        'time': time,
                    }

                    return render(request, 'attribution/attribution_error_page_before.html', data)
                else:
                    # print(cancel_scheduled_task())
                    queue = TeacherQueuePosition.objects.filter(blockk=blockk).order_by('position').all()
                    value = str(float_to_time(int(get_time_left())))

                    data = {
                        'queue': queue,
                        'blockk': blockk,
                        'time_left': value,
                    }
                    return render(request, 'attribution/attribution.html', data)
            else:

                data = {
                    'day': None,
                    'time': None,
                }

                return render(request, 'attribution/attribution_error_page_before.html')
        else:
            queue = TeacherQueuePosition.objects.filter(blockk=blockk).order_by('position').all()
            # value = str(float_to_time(int(get_time_left())))
            # print(value)

            data = {
                'queue': queue,
                'blockk': blockk,
                # 'time_left': value,
            }
            return render(request, 'attribution/attribution.html', data)
            
    if request.method == 'POST':
        queue = TeacherQueuePosition.objects.filter(blockk=blockk).order_by('position').all()
        next_professor = queue.get(blockk=blockk, position=0)

        attribution_preference = Attribution_preference.objects.filter(user=next_professor.teacher).all()
        if attribution_preference:
            timetables_preference = Course_preference.objects.filter(attribution_preference=attribution_preference).all()
        if request.User == next_professor:            
            next_attribution(timetables_preference, next_professor, blockk)    

    return render(request, 'attribution/attribution.html')

def timestup(professor, blockk):
    if TeacherQueuePosition.objects.count() > 1:
        professor_to_end_queue(professor, blockk)
        start_attribution(blockk)
    else:
        TeacherQueuePosition.objects.filter(teacher=professor, blockk=blockk).delete()
        Deadline.objects.filter(blockk=blockk, name='STARTASSIGNMENTDEADLINE').update(deadline_end=datetime.datetime.now())

def start_attribution(blockk):
    if TeacherQueuePosition.objects.filter(blockk=blockk).exists():
        queue = TeacherQueuePosition.objects.filter(blockk=blockk).order_by('position').all()
        next_professor_in_queue = queue.get(blockk=blockk, position=0)

        attribution_preference = Attribution_preference.objects.get(user=next_professor_in_queue.teacher)
        if attribution_preference:
            timetables_preference = Course_preference.objects.filter(attribution_preference=attribution_preference).all()

        next_attribution(timetables_preference, next_professor_in_queue, blockk)
    else:
        Deadline.objects.filter(blockk=blockk, name='STARTASSIGNMENTDEADLINE').update(deadline_end=datetime.datetime.now())

def next_attribution(timetables_preference, next_professor_in_queue, blockk):
    print(f'Analisando professor { next_professor_in_queue.teacher.first_name }')
    
    professor = next_professor_in_queue.teacher

    fpa_current_user = Attribution_preference.objects.get(user=professor)

    primary_timetable_ids = Course_preference.objects.filter(priority=Priority.primary.name, blockk=blockk, attribution_preference=fpa_current_user).values_list('timetable', flat=True)
    secondary_timetable_ids = Course_preference.objects.filter(priority=Priority.secondary.name, blockk=blockk, attribution_preference=fpa_current_user).values_list('timetable', flat=True)

    other_primary_timetables_ids = Course_preference.objects.filter(priority=Priority.primary.name, attribution_preference=fpa_current_user).exclude(blockk=blockk).values_list('timetable', flat=True)


    primary_timetable = ids_to_timetables(primary_timetable_ids)
    secondary_timetable = ids_to_timetables(secondary_timetable_ids)
    other_primary_timetables = ids_to_timetables(other_primary_timetables_ids)

    cord_other_timetables = []

    for timetable in other_primary_timetables:
        cord_other_timetables.extend(create_cord(timetable))

    cord_primary_timetables = []
    for timetable in primary_timetable:
        cord_primary_timetables.extend(create_cord(timetable))

    SECONDS_TO_PROFESSOR_CHOOSE = 50
    
    invalidated_timetables = []
    
    cord_assigned_timetables = []

    for timetable in primary_timetable:
        if validate_timetable(timetable, professor) != True:
            print(f'professor { professor.first_name }: [{ timetable.course }] primária: falhou')
        else:
            print(f'professor { professor.first_name }: [{ timetable.course }] primária: sucesso')
            assign_timetable_professor(timetable, professor)
            cord_assigned_timetables.extend(create_cord(timetable))

    for timetable in secondary_timetable:
        qnt_primary = len(cord_primary_timetables)
        qnt_timetables_assigned = len(cord_assigned_timetables)
        
        timetable_cord = create_cord(timetable)

        if (qnt_timetables_assigned + len(timetable_cord)) <= qnt_primary:

            if not set(timetable_cord).intersection(cord_assigned_timetables) or not set(timetable_cord).intersection(cord_other_timetables):

                if validate_timetable(timetable, professor) != True:
                    print(f'Professor { professor.first_name }: [{ timetable.course }] secundária: falhou')
                    invalidated_timetables.append(timetable)
                else:
                    print(f'Professor { professor.first_name }: [{ timetable.course }] secundária: sucesso')
                    cord_assigned_timetables.extend(timetable_cord)
                    assign_timetable_professor(timetable, professor)
            

    other_secondary_timetables = timetables_preference.filter(priority=Priority.secondary.name, attribution_preference=fpa_current_user).exclude(blockk=blockk).values_list('timetable', flat=True)


    if not other_secondary_timetables or other_primary_timetables:

        if len(cord_assigned_timetables) < len(cord_primary_timetables):
            print(f'professor { professor.first_name }: faltou aulas para cumprir a quantidade desejada')
            # send_email(professor)
            print(f'professor { professor.first_name }: entrando em atribuição manual')
            schedule_task(SECONDS_TO_PROFESSOR_CHOOSE, professor, blockk, blockk.registration_block_id)
            return
        elif len(invalidated_timetables) == 0:
            professor_to_end_queue(professor, blockk)
            next_professor_in_queue.delete()
            cancel_scheduled_task('task')
            print(f'professor { professor.first_name }: atribuição finalizada com sucesso!')
            return start_attribution(blockk)
        else:
            print(f'professor { professor.first_name }: entrando em atribuição manual')
            # send_email(professor)
            schedule_task(SECONDS_TO_PROFESSOR_CHOOSE, professor, blockk, blockk.registration_block_id)
            return
    else:
        if len(cord_assigned_timetables) < len(cord_primary_timetables):
            print(f'professor { professor.first_name }: faltou aulas para cumprir a quantidade desejada')
            # send_email(professor)
            schedule_task(SECONDS_TO_PROFESSOR_CHOOSE, professor, blockk, blockk.registration_block_id)
            return
        professor_to_end_queue(professor, blockk)
        next_professor_in_queue.delete()
        cancel_scheduled_task('task')
        print(f'professor { professor.first_name }: atribuição finalizada com sucesso!')
        return start_attribution(blockk)

def ids_to_timetables(ids):
    timetables = []
    for id in ids:
        timetables.append(Timetable.objects.get(id=id))
    return timetables

def create_cord(timetable):
    day_combos = timetable.day_combo.all()

    list_cords = []

    for day_combo in day_combos:
        day = day_combo.day
        timeslots = day_combo.timeslots.all()

        for timeslot in timeslots:
            position = timeslot.position
            cord = f'{position}-{day}'
            list_cords.append(cord)

    return list_cords

def validate_timetable(timetable, professor):
    if validations(timetable, professor):
        return True
    else:
        return timetable

def validations(timetable, professor):
    timetable_user = None
    if Timetable_user.objects.filter(timetable=timetable).exists():
        timetable_user = Timetable_user.objects.get(timetable=timetable)
    else:
        timetable_user = Timetable_user.objects.create(timetable=timetable, user=None)
    if timetable_user.user is not None:
        return False
    course = timetable.course
    return Proficiency.objects.get(user=professor, course=course).is_competent
    # future validations

@login_required
def email_test(request):
    if request.method == 'POST':
        superusers = User.objects.filter(is_superuser=True).all()
        for superuser in superusers:
            send_email(superuser)

        return redirect('attribution:email_test')
    return render(request, 'attribution/email_test.html')

def send_email(professor):
    print(f'Enviando email para { professor.first_name }')
    subject = 'Ação requerida: Escolha de disciplina alternativa até o prazo estipulado'
    
    nome = professor.first_name
    email = professor.email

    current_path = os.getcwd()
    with open(current_path + '\\templates\static\email\message.html', 'r', encoding='utf-8') as file:
        message = file.read()
        message = message.format(nome=nome)
    
    email = EmailMessage(
        subject,
        message,
        'ada.ifsp@gmail.com',
        [email],
    )

    email.content_subtype = "html"

    email.send()

def assign_timetable_professor(timetable, professor):
    Timetable_user.objects.filter(timetable=timetable).update(user=professor)

def professor_to_end_queue(professor, blockk):

    size_queue = len(TeacherQueuePosition.objects.filter(blockk=blockk).all())

    TeacherQueuePosition.objects.filter(teacher=professor, blockk=blockk).update(position=size_queue )

    for professor_in_queue in TeacherQueuePosition.objects.filter(blockk=blockk).all():
        professor_in_queue.position = professor_in_queue.position - 1
        professor_in_queue.save()

def float_to_time(seconds):
    print(seconds)
    if seconds < 0:
        seconds = 0
    delta = timedelta(seconds=seconds)
    time = datetime.datetime(1, 1, 1) + delta
    return time.time()

def schedule_attributtion_deadline_staff(seconds, name, queue,*args):
    # cancel_scheduled_task('task')
    schedule_deadline(attribution_deadline_start, seconds, name, queue, *args)


import datetime
def manual_attribution(request):   

    if request.method == 'POST':
        get_block = request.POST.get('blockk')
        blockk = Blockk.objects.get(registration_block_id=get_block)
        print(blockk)

        work_courses = request.POST.get('timetable')

        data = json.loads(work_courses);

        result = []
        for item in data:
            temp_dict = {
                'id_timetable': item['id_timetable'],
                'position': item['position']
            }
            result.append(temp_dict)

        timetables = []
        for item in result:
            timetables.append(Timetable.objects.get(id=item['id_timetable']))

        timetables_invalidate = manual_attribution_save(timetables, request.user, blockk)

        # print(timetables_invalidate)

        if timetables_invalidate == False:
            return JsonResponse({'redirect_url': '/atribuicao/atribuicao-manual-erro'}) 
        elif timetables_invalidate != None:
            return render(request, 'attribution/manual_attribution.html')
        else:
            
            return JsonResponse({'redirect_url': '/atribuicao/atribuicao-manual-confirmar/?blockk='+str(blockk.registration_block_id)}) 
    else:
        user = request.user
        get_block = request.GET.get('blockk')
        blockk = Blockk.objects.get(registration_block_id=get_block)
        if TeacherQueuePosition.objects.get(position=0, blockk=blockk).teacher != user:
            base_url = reverse('attribution:attribution')
            target_url = f'{base_url}?blockk={blockk.registration_block_id}'

            return redirect(target_url)

        user_regime = user.job
        courses = Course.objects.all()
        user_is_fgfcc = False
        user_is_fgfcc = user.is_fgfcc
        
        user_block = Blockk.objects.get(registration_block_id=request.GET.get('blockk'))
        timetables_current_user = Timetable_user.objects.filter(user=user, timetable__course__blockk=user_block).all()

        dias_semana = {
            'monday': 'mon',
            'tuesday': 'tue',
            'wednesday': 'wed',
            'thursday': 'thu',
            'friday': 'fri',
            'saturday': 'sat'
        }

        timetable_current_user_array = []
        if timetables_current_user:
            for timetable_object in timetables_current_user:
                timetable = timetable_object.timetable
                day_combo_objects = timetable.day_combo.all()

                for day_combo in day_combo_objects:
                    day = day_combo.day
                    timeslots = day_combo.timeslots.all()

                    for timeslot in timeslots:
                        turno = None

                        if timeslot.hour_start >= datetime.time(7, 0, 0) and timeslot.hour_end <= datetime.time(12, 0, 0):
                            turno = 'mor'
                        elif timeslot.hour_start >= datetime.time(13, 0, 0) and timeslot.hour_end <= datetime.time(18, 0, 0):
                            turno = 'aft'
                        elif timeslot.hour_start >= datetime.time(18, 0, 0) and timeslot.hour_end <= datetime.time(23, 0, 0):
                            turno = 'noc'

                        posicao = timeslot.position

                        if posicao > 12:
                            posicao_calc = posicao - 12
                        elif posicao > 6:
                            posicao_calc = posicao - 6
                        else:
                            posicao_calc = posicao

                        course_name = timetable.course.name_course
                        course_acronym = timetable.course.acronym
                        day_string = dias_semana[day]

                        timetable_item = {
                            'phrase': f'{day_string}-{turno}-{posicao_calc}', #sub-fri-mat-4
                            'course_acronym': course_acronym,
                            'course_name': course_name,
                        }
                        timetable_current_user_array.append(timetable_item)

        user_timetable = []
        timetables_without_user = []
        timetables_user_without_user = Timetable_user.objects.filter(user=None)
        for timetable_user_without_user in timetables_user_without_user:
            timetable_without_user = timetable_user_without_user.timetable 
            timetables_without_user.append(timetable_without_user)

        timetables_without_user_blockk = []
        for timetable_user_without_user in timetables_without_user:
            timetable_without_user_same_blockk = Timetable.objects.filter(course__blockk=user_block).filter(id=timetable_user_without_user.id).first()
            timetables_without_user_blockk.append(timetable_without_user_same_blockk)
        # delete de timetables_without_user_blockk todos none
        timetables_without_user_blockk = list(filter(None, timetables_without_user_blockk))

        print(timetables_without_user_blockk)
        for timetable_object in timetables_without_user_blockk:
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
        
        if user_regime.name_job == "RDE" or user_regime.name_job == "FORTY_HOURS" or user_regime.name_job == "TEMPORARY":
            user_regime_choosed = user_regime
            user_regime_choosed.name_job = '40'
        elif user_regime.name_job == "TWENTY_HOURS" or user_regime.name_job == "SUBSTITUTE":
            user_regime_choosed = user_regime
            user_regime_choosed.name_job = '20'
        else:
            user_regime_choosed = user_regime

        user_timeslot_table = []
        horarios = {
            "mor": ["07:00:01", "07:45:01", "08:30:01", "09:30:01", "10:15:01", "11:00:01"],
            "aft": ["13:15:01", "14:00:01", "14:45:01", "15:45:01", "16:30:01", "17:15:01"],
            "noc": ["18:00:01", "18:50:01", "19:35:01", "20:20:01", "21:05:01", "21:50:01"],
        }

        dias_semana = ["mon", "tue", "wed", "thu", "fri", "sat"]

        for dia in dias_semana:
            for shift_type, horario in horarios.items():
                for position, timeslot_begin_hour in enumerate(horario, start=1):
                    string = {
                        "id": f"{dia}-{shift_type}-{position}",
                        "position": position,
                        "type": shift_type,
                        "day": dia,
                        "timeslot_begin_hour": timeslot_begin_hour,
                    }
                    user_timeslot_table.append(string)

    print(user_timeslot_table)

    data = {
        'user_regime': user_regime_choosed,
        'user_is_fgfcc': user_is_fgfcc,
        'shift': shift,
        'ids': user_timeslot_table,
        'user_blockk': user_block, # apenas um block
        'user_current_timetables': timetable_current_user_array,
        'user_timetables': user_timetable, # pega todos nao atribuidos e dps pega so do bloco
        'user_courses': user_courses,
    }

    return render(request, 'attribution/manual_attribution.html', data)

@transaction.atomic
def manual_attribution_save(timetables, professor, blockk):
    print(f'Atual professor {TeacherQueuePosition.objects.get(position=0, blockk=blockk).teacher.first_name} e professor sendo atualizado {professor.first_name}')
    if TeacherQueuePosition.objects.get(position=0, blockk=blockk).teacher == professor:
        print(timetables)
        invalidated_timetables = []

        for timetable in timetables:
            if validate_timetable(timetable, professor) != True:
                print(f'professor { professor.first_name } não pode escolher a grade { timetable.course }')
                invalidated_timetables.append(timetable)
            else:
                assign_timetable_professor(timetable, professor)
    
        if len(invalidated_timetables) == 0:
            professor_to_end_queue(professor, blockk)
            TeacherQueuePosition.objects.filter(teacher=professor, blockk=blockk).delete()
            
            print(f'Professor { professor.first_name } escolheu suas novas aulas com sucesso!')
            return None
        else:        
            return invalidated_timetables
    else:
        return False
    
@login_required
def manual_attribution_timesup(request):
    
    return render(request, 'attribution/manual_attribution_timesup.html')

@login_required
def manual_attribution_confirm(request):
    blockk = Blockk.objects.get(registration_block_id=request.GET.get('blockk'))
    cancel_scheduled_task('task')
    start_attribution(blockk)

    return render(request, 'attribution/manual_attribution_confirm.html')

@login_required
def attribution_class_list(request, blockk):
    areas = Blockk.objects.get(registration_block_id=blockk).areas.all()
    print(f'Areas: {areas}')
    classses = Classs.objects.filter(area__in=areas).all()
    print(f'Classses: {classses}')
    data = {
        'classses': classses,
    }

    return render(request, 'attribution/attribution_class_list.html', data)

@login_required
def attribution_detail(request):
    classs = Classs.objects.get(registration_class_id=request.GET.get('class'))
    timetables = Timetable.objects.filter(classs=classs).all()
    timeslots_all = Timeslot.objects.all()
    timetables_user = Timetable_user.objects.filter(timetable__in=timetables).all()

    timetables_professor = []
    
    for timetable_user in timetables_user:
        day_combos = timetable_user.timetable.day_combo.all()
        for day_combo in day_combos:
            day = day_to_number(day_combo.day)
            timeslots = day_combo.timeslots.all()

            if timetable_user.user is not None:
                professor = timetable_user.user.first_name
            else:
                professor = "-"

            for timeslot in timeslots:

                position = timeslot.position
                print(timetable_user.user)
                timetable_professor = {
                    "cord": f'{position}-{day}',
                    "course": timetable_user.timetable.course.name_course,
                    "acronym": timetable_user.timetable.course.acronym,
                    "professor": professor,
                }
                timetables_professor.append(timetable_professor)
    timetables_professor_json = json.dumps(timetables_professor, ensure_ascii=False).encode('utf8').decode()

    data = {
        'timeslots': timeslots_all,
        'timetables_professor': timetables_professor_json,
        'classs': classs
    }
    return render(request, 'attribution/attribution_detail.html', data)

def remove_professors_without_preference(blockk):
    queue = TeacherQueuePosition.objects.filter(blockk=blockk).order_by('position').all()
    for professor_in_queue in queue:
        if not Attribution_preference.objects.filter(user=professor_in_queue.teacher).exists():
            professor_in_queue.delete()
    return

