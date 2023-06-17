from area.models import Blockk
from attribution.task import attribution_deadline_start, cancel_scheduled_task, get_time_left, schedule_task, schedule_deadline
from staff.models import Criteria, Deadline
from timetable.models import Timetable, Timetable_user
from user.models import User
from attribution.models import TeacherQueuePosition
from django.shortcuts import render, redirect
import json
from django.db.models import F, Sum, Value
from django.db import transaction
from django.utils import timezone
from datetime import datetime, timedelta, timezone
from django.core.mail import send_mail, EmailMessage
import xml.etree.ElementTree as ET
import os

from attribution_preference.models import Course_preference, Attribution_preference

from django.utils.decorators import method_decorator

TEMPO_LIMITE_SEGUNDOS = 10 

def attribution(request):
    
    blockk = Blockk.objects.get(registration_block_id=request.GET.get('blockk'))
   
    
    if request.method == 'GET':
        print(get_time_left())
        # print(cancel_scheduled_task())
        queue = TeacherQueuePosition.objects.filter(blockk=blockk).order_by('position').all()
        value = str(float_to_time(int(get_time_left())))
        print(value)

        data = {
            'queue': queue,
            'blockk': blockk,
            'time_left': value,
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
    professor_to_end_queue(professor)
    start_attribution(blockk)

def start_attribution(blockk):
    print('oier')
    queue = TeacherQueuePosition.objects.filter(blockk=blockk).order_by('position').all()
    next_professor_in_queue = queue.get(blockk=blockk, position=0)

    attribution_preference = Attribution_preference.objects.get(user=next_professor_in_queue.teacher)
    if attribution_preference:
        timetables_preference = Course_preference.objects.filter(attribution_preference=attribution_preference).all()

    next_attribution(timetables_preference, next_professor_in_queue, blockk)

def next_attribution(timetables_preference, next_professor_in_queue, blockk):
    timetables_id = timetables_preference.values_list('timetable', flat=True)
    professor = next_professor_in_queue.teacher

    timetables = []

    for timetable_id in timetables_id:
        timetables.append(Timetable.objects.get(id=timetable_id))   
    print(timetables)
    SECONDS_TO_PROFESSOR_CHOOSE = 10
    
    invalidated_timetables = []

    print(f'tamanho da lista de grades: { len(timetables) }')

    for timetable in timetables:
        if validate_timetable(timetable, professor) != True:
            invalidated_timetables.append(timetable)
        else:
            assign_timetable_professor(timetable, professor)
            
    if len(invalidated_timetables) == 0:
        professor_to_end_queue(professor)
        next_professor_in_queue.delete()
        cancel_scheduled_task()
        return start_attribution(blockk)
    else:
        # send_email(professor)
        schedule_task(SECONDS_TO_PROFESSOR_CHOOSE, professor, blockk)
        return

def validate_timetable(timetable, professor):
    if validations(timetable, professor):
        return True
    else:
        return timetable

def validations(timetable, professor):
    print(timetable)
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

    print(f'size: {size_queue}')
    
    TeacherQueuePosition.objects.filter(teacher=professor).update(position=size_queue )
    for professor_in_queue in TeacherQueuePosition.objects.all():
        professor_in_queue.position = professor_in_queue.position - 1
        professor_in_queue.save()
        print(f'professor: {professor_in_queue.teacher.first_name} - position: {professor_in_queue.position}')        

def float_to_time(seconds):
    print(seconds)
    if seconds < 0:
        seconds = 0
    delta = timedelta(seconds=seconds)
    time = datetime(1, 1, 1) + delta
    return time.time()

def schedule_attributtion_deadline_staff(seconds, name, *args):
    cancel_scheduled_task('task')
    schedule_deadline(attribution_deadline_start, seconds, name, *args)