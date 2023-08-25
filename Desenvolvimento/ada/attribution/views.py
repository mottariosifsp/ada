from django.http import JsonResponse
from area.models import Area, Blockk
from attribution.task import attribution_deadline_start, cancel_all_tasks, cancel_scheduled_task, get_time_left, schedule_task, schedule_deadline
from attribution_preference.views import convert_string_to_datetime, save_disponiility_preference
from classs.models import Classs
from course.models import Course
from staff.models import Criteria, Deadline
from timetable.models import Timeslot, Timetable, Timetable_user
from user.models import User
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
        professor_to_end_queue(professor)
        start_attribution(blockk)
    else:
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

    primary_timetable_ids = timetables_preference.filter(priority="PRIMARY", blockk=blockk).values_list('timetable', flat=True)
    secondary_timetable_ids = timetables_preference.filter(priority="SECONDARY", blockk=blockk).values_list('timetable', flat=True)

    other_primary_timetables_ids = timetables_preference.filter(priority="PRIMARY", blockk__ne=blockk).values_list('timetable', flat=True)

    primary_timetable = ids_to_timetables(primary_timetable_ids)
    secondary_timetable = ids_to_timetables(secondary_timetable_ids)
    other_primary_timetables = ids_to_timetables(other_primary_timetables_ids)

    cord_other_timetables = []

    for timetable in other_primary_timetables:
        cord_other_timetables.extend(create_cord(timetable))

    professor = next_professor_in_queue.teacher

    SECONDS_TO_PROFESSOR_CHOOSE = 50
    
    invalidated_timetables = []

    cord_assigned_timetables = []

    for timetable in primary_timetable:
        if validate_timetable(timetable, professor) != True:
            invalidated_timetables.append(timetable)
        else:
            assign_timetable_professor(timetable, professor)
            cord_assigned_timetables.extend(create_cord(timetable))

    for timetable in secondary_timetable:
        
        timetable_cord = create_cord(timetable)

        if set(timetable_cord).intersection(cord_assigned_timetables) or set(timetable_cord).intersection(cord_other_timetables):

            if validate_timetable(timetable, professor) != True:
                invalidated_timetables.append(timetable)
            else:
                assign_timetable_professor(timetable, professor)

    other_secondary_timetables = timetables_preference.filter(priority="SECONDARY", blockk__ne=blockk).values_list('timetable', flat=True)

    if not other_secondary_timetables or other_primary_timetables:
        if len(invalidated_timetables) == 0:
            professor_to_end_queue(professor)
            next_professor_in_queue.delete()
            cancel_scheduled_task('task')
            print(f'Atribuição do professor { professor.first_name } finalizada com sucesso!')
            return start_attribution(blockk)
        else:
            print(f'Conflito na atribuição do professor { professor.first_name }')
            # send_email(professor)
            schedule_task(SECONDS_TO_PROFESSOR_CHOOSE, professor, blockk)
            return
    else:
        professor_to_end_queue(professor)
        next_professor_in_queue.delete()
        cancel_scheduled_task('task')
        print(f'Atribuição do professor { professor.first_name } no bloco { blockk } finalizada, aguardando atribuição de outros blocos')
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
    if timetable_user.user is None:
        return True
    else:
        return False
    # future validations

def email_test(request):
    if request.method == 'POST':
        superusers = User.objects.filter(is_superuser=True).all()
        for superuser in superusers:
            send_email(superuser)

        return redirect('attribution:email_test')
    return render(request, 'attribution/email_test.html')

def send_email(professor):
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
    print(f'professor { professor.first_name } escolheu a grade { timetable }')
    Timetable_user.objects.filter(timetable=timetable).update(user=professor)

def professor_to_end_queue(professor):

    size_queue = len(TeacherQueuePosition.objects.all())
    
    TeacherQueuePosition.objects.filter(teacher=professor).update(position=size_queue )
    for professor_in_queue in TeacherQueuePosition.objects.all():
        professor_in_queue.position = professor_in_queue.position - 1
        professor_in_queue.save()

def float_to_time(seconds):
    print(seconds)
    if seconds < 0:
        seconds = 0
    delta = timedelta(seconds=seconds)
    time = datetime.datetime(1, 1, 1) + delta
    return time.time()

def schedule_attributtion_deadline_staff(seconds, name, *args):
    cancel_scheduled_task('task')
    schedule_deadline(attribution_deadline_start, seconds, name, *args)

import datetime
def manual_attribution(request):   

    if request.method == 'POST':
        blockk = Blockk.objects.get(registration_block_id=request.POST.get('blockk'))

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

        print(timetables_invalidate)

        if timetables_invalidate == False:
            return JsonResponse({'redirect_url': '/atribuicao/atribuicao-manual-erro'}) 
        elif timetables_invalidate != None:
            return render(request, 'attribution/manual_attribution.html')
        else:
            
            return JsonResponse({'redirect_url': '/atribuicao/atribuicao-manual-confirmar/?blockk='+str(blockk.registration_block_id)}) 
    else:
        blockk = Blockk.objects.get(registration_block_id=request.GET.get('blockk'))
        user = request.user
        timetables_user = Timetable_user.objects.filter(user=None).all()

        timetables_current_user = Timetable_user.objects.filter(user=user).all()

        # print(timetables_current_user)

        timetable = []
        courses = []
        timetable_user_c = []

        for timetable_current_user in timetables_current_user:
            timetable_user_c.append(timetable_current_user.timetable)

        # print(timetable_user_c)

        for timetable_user in timetables_user:
            courses.append(timetable_user.timetable.course)

        for timetable_user in timetables_user:
            timetable.append(timetable_user.timetable)

        blocks = user.blocks.all().distinct()
        areas = Area.objects.filter(blocks__in=blocks).distinct()

        user_area = []
        user_blocks = []

        for area in areas:
            area_obj = {
                'id': area.registration_area_id,
                'name_area': area.name_area,
                'acronym': area.acronym,
                'blocks': [block.registration_block_id for block in area.blocks.all()]
            }
            user_area.append(area_obj)

        for block in blocks:
            block_obj = {
                'id': block.registration_block_id,
                'name_block': block.name_block,
                'acronym': block.acronym
            }
            user_blocks.append(block_obj)

        user_blocks_ids = [int(block['id']) for block in user_blocks]

        timetable_array = []

        for id_block in user_blocks_ids:
            for timetable_object in Timetable.objects.filter(course__blockk=id_block):
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


            timetable_array.append(timetable_item)

        timetable_user_array = []

        dias_semana = {
            'monday': 'mon',
            'tuesday': 'tue',
            'wednesday': 'wed',
            'thursday': 'thu',
            'friday': 'fri',
            'saturday': 'sat'
        }

        if timetable_user_c:
            for timetable_object in timetable_user_c:
                day_combo_objects = timetable_object.day_combo.all()

                for day_combo in day_combo_objects:
                    day = day_combo.day
                    timeslots = day_combo.timeslots.all()

                    for timeslot in timeslots:
                        turno = None

                        if timeslot.hour_start >= datetime.time(7, 0, 0) and timeslot.hour_end <= datetime.time(12, 0, 0):
                            turno = 'mat'
                        elif timeslot.hour_start >= datetime.time(13, 0, 0) and timeslot.hour_end <= datetime.time(18, 0, 0):
                            turno = 'ves'
                        elif timeslot.hour_start >= datetime.time(18, 0, 0) and timeslot.hour_end <= datetime.time(23, 0, 0):
                            turno = 'not'

                        posicao = timeslot.position

                        if posicao > 12:
                            posicao_calc = posicao - 12
                        elif posicao > 6:
                            posicao_calc = posicao - 6
                        else:
                            posicao_calc = posicao

                        course_name = timetable_object.course.name_course
                        course_acronym = timetable_object.course.acronym
                        day_string = dias_semana[day]

                        timetable_item = {
                            'phrase': f'{day_string}-{turno}-{posicao_calc}', #sub-fri-mat-4
                            'course_acronym': course_acronym,
                            'course_name': course_name,
                        }

                        timetable_user_array.append(timetable_item)

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
        timeslots = Timeslot.objects.all()

        dias_semana = {
            'monday': 'mon',
            'tuesday': 'tue',
            'wednesday': 'wed',
            'thursday': 'thu',
            'friday': 'fri',
            'saturday': 'sat'
        }

        for dia in dias_semana.values():
            for posicao in range(1, 19):  # 18 horários possíveis
                timeslot = timeslots[posicao-1]  # Assumindo que timeslots esteja ordenado corretamente

                if timeslot.hour_start < datetime.time(12, 0, 0):
                    turno_sessao = 'mat'
                elif timeslot.hour_start < datetime.time(18, 0, 0):
                    turno_sessao = 'ves'
                else:
                    turno_sessao = 'not'
                if posicao > 12:
                    posicao_calc = posicao - 12
                elif posicao > 6:
                    posicao_calc = posicao - 6
                else:
                    posicao_calc = posicao
                string = {
                    'frase': f'{dia}-{turno_sessao}-{posicao_calc}',
                    'posicao': posicao_calc,
                    'sessao': turno_sessao,
                    'dia': dia,
                    'hour': timeslot.hour_start.strftime('%H:%M:%S'),
                }
                user_timeslot_traceback.append(string)

        print(user_timeslot_traceback)

        regime = request.user.job
        
        data = {
            'regime': regime,
            'turno': turno,
            'user_disponibility': user_timeslot_traceback,
            'user_blocks': user_blocks,
            'user_areas': user_area,
            'timetables': timetable_array,
            'courses': courses_array,
            'timetables_user': timetable_user_array,
            'blockk': blockk,
        }

        return render(request, 'attribution/manual_attribution.html', data)

def manual_attribution_save(timetables, professor, blockk):
    print(f'Atual professor {TeacherQueuePosition.objects.get(position=0).teacher.first_name} e professor sendo atualizado {professor.first_name}')
    if TeacherQueuePosition.objects.get(position=0).teacher == professor:
        invalidated_timetables = []

        for timetable in timetables:
            if validate_timetable(timetable, professor) != True:
                invalidated_timetables.append(timetable)
            else:
                assign_timetable_professor(timetable, professor)
    
        if len(invalidated_timetables) == 0:
            professor_to_end_queue(professor)
            TeacherQueuePosition.objects.filter(teacher=professor).delete()
            
            print(f'Professor { professor.first_name } escolheu suas novas aulas com sucesso!')
            return None
        else:        
            return invalidated_timetables
    else:
        return False

def manual_attribution_timesup(request):
    
    return render(request, 'attribution/manual_attribution_timesup.html')

def manual_attribution_confirm(request):
    blockk = Blockk.objects.get(registration_block_id=request.GET.get('blockk'))
    cancel_scheduled_task('task')
    start_attribution(blockk)

    return render(request, 'attribution/manual_attribution_confirm.html')

def attribution_class_list(request, blockk):
    areas = Blockk.objects.get(registration_block_id=blockk).areas.all()
    print(f'Areas: {areas}')
    classses = Classs.objects.filter(area__in=areas).all()
    print(f'Classses: {classses}')
    data = {
        'classses': classses,
    }

    return render(request, 'attribution/attribution_class_list.html', data)

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

