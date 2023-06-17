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

marcador = 0
tabela_data = ""

# Seleciona o campo marcado pelo administrador e verifica qual é o atributo correspondente no histórico dos usuários
def get_selected_campo():
    if Criteria.objects.filter(is_select=True).exists():
        valor_numero = Criteria.objects.filter(is_select=True).values('number_criteria').first().get('number_criteria')

        if valor_numero in range(1, 8): # 1-7, exclui o 8
            campos = {
                1: 'birth',
                2: 'date_career',
                3: 'date_campus',
                4: 'date_professor',
                5: 'date_area',
                6: 'date_institute',
                7: 'academic_degrees'
            }

            return campos.get(valor_numero, "campo")
        else:
            return ""
    else:
        return ""

def add_teacher_to_queue(teacher, position_input, blockk):
    position = position_input
    TeacherQueuePosition.objects.create(teacher=teacher, position=position, blockk=blockk)
    print(f'professor { teacher.first_name } adicionado na fila com a posição { position } no bloco { blockk }')

# View que leva para a(s) fila(s) já definida pelo admin
def queue(request):
    campo = get_selected_campo()

    teacher_positions = TeacherQueuePosition.objects.order_by('position')

    total_scores = []

    for teacher_position in teacher_positions:
        user = teacher_position.teacher
        history = user.history
        total_score = history.academic_degrees.aggregate(total_score=Sum('punctuation'))['total_score']
        total_scores.append(total_score)

    resultados = teacher_positions.select_related('teacher').order_by('position').all()

    data = {
        'resultados': resultados,
        'total_scores': total_scores,
        'campo': campo,
    }

    return render(request, 'attribution/queue.html', {'data': data})

# View que leva para a página de definir a fila
def queueSetup(request):
    global marcador
    global tabela_data # variável utilizada caso a fila já tenha sido definida pelo menos uma vez pelo admin

    if request.method == 'POST': # adiciona os professores no model TeacherQueuePosition
        tabela_data = json.loads(request.POST['tabela_data'])
        blockk = Blockk.objects.get(registration_block_id=request.POST['blockk_id'])
        campo = get_selected_campo()

        for professorInQueue in tabela_data:
            professor_registration_id = professorInQueue[1]
            position = professorInQueue[0]
            professor = User.objects.get(registration_id=professor_registration_id)

            if TeacherQueuePosition.objects.filter(teacher=professor, blockk=blockk).exists():
                TeacherQueuePosition.objects.filter(teacher=professor).update(position=position)
            else:
                add_teacher_to_queue(professor, position, blockk)

        data = {
            'resultados': TeacherQueuePosition.objects.select_related('teacher').order_by('position').all(),
            'campo': campo,
        }

        return render(request, 'attribution/queueSetup.html', {'data': data})

    else: # se a requisição não for POST e for GET sem ter passado a área, ou seja, sem ter atualização no filtro da área, vai cair aqui
        blockk = Blockk.objects.get(registration_block_id=request.GET.get('blockk'))
        
        if TeacherQueuePosition.objects.filter(blockk=blockk).exists(): # se já tiver uma tabela criada para a área selecionada
            campo = get_selected_campo()

            teacher_positions = TeacherQueuePosition.objects.filter(blockk=blockk).order_by('position')

            all_users = User.objects.all()
            
            missing_users = []

            for user in all_users:
                if not teacher_positions.filter(teacher=user).exists():
                    if user.is_professor:
                        if user.blocks.filter(registration_block_id=blockk.registration_block_id).exists(): 
                            missing_users.append(user)

                final_list = list(teacher_positions) + missing_users

                usuarios_somados = []

                for item in final_list:
                    if isinstance(item, TeacherQueuePosition):
                        user = item.teacher
                        if user is not None and user.history is not None:
                            total_score = user.history.academic_degrees.aggregate(total_score=Sum('punctuation'))[
                                'total_score']
                        else:
                            total_score = 0
                    else:
                        user = item
                        if user is not None and user.history is not None:

                            total_score = user.history.academic_degrees.aggregate(total_score=Sum('punctuation'))[
                                'total_score']
                        else:
                            total_score = 0
                    user.total_score = total_score
                    usuarios_somados.append(user)
            data = {
                'resultados': final_list,
                'campo': campo,
                'total_score': usuarios_somados,
                'blockk': blockk
            }

            return render(request, 'attribution/queueSetup.html', {'data': data})

        if Criteria.objects.filter(is_select=True).exists():
            campo = get_selected_campo()

            if campo != "":

                usuarios_ordenados = User.objects.filter(is_professor=True,blocks=blockk).order_by(f'history__{campo}')

                # Faz a soma dos academic degrees para cada usuário
                usuarios_somados = usuarios_ordenados.annotate(total_score=Sum('history__academic_degrees__punctuation'))

                data = {
                    'resultados': usuarios_ordenados,
                    'campo': campo,
                    'total_score': usuarios_somados,
                    'blockk': blockk
                }
                
                return render(request, 'attribution/queueSetup.html', {'data': data})

            else: # se o superadmin selecionou um critério que não tenha relação com nenhum atributo do histórico vai cair aqui
                  # fazer exception?

                usuarios_ordenados = User.objects.filter(is_professor=True,blocks=blockk).all()

                usuarios_somados = usuarios_ordenados.annotate(total_score=Sum('history__academic_degrees__punctuation'))
                data = {
                    'resultados': usuarios_ordenados,
                    'campo': campo,
                    'total_score': usuarios_somados,
                    'blockk': blockk
                }

                return render(request, 'attribution/queueSetup.html', {'data': data})

        # se nenhum critério foi selecionado pelo adm e não tiver feito nenhuma lista manual vai cair aqui
        campo = get_selected_campo()

        usuarios_ordenados = User.objects.all()
        usuarios_somados = usuarios_ordenados.annotate(total_score=Sum('history__academic_degrees__punctuation'))
        
        data = {
            'resultados': usuarios_ordenados,
            'campo': campo,
            'total_score': usuarios_somados,
            'blockk': blockk
        }

        return render(request, 'attribution/queueSetup.html', {'data': data})  
     
def attribution(request):
    
    blockk = Blockk.objects.get(registration_block_id=request.GET.get('blockk'))
   
    
    if request.method == 'GET':
        attribution_deadline = Deadline.objects.get(blockk=blockk, name='STARTASSIGNMENTDEADLINE')
        now = datetime.today()
        if now > attribution_deadline.deadline_end:
            return render(request, 'attribution/attribution_error_page_after.html')
        if now < attribution_deadline.deadline_start:            
            day = attribution_deadline.deadline_start.strftime("%d/%m/%Y")
            time = attribution_deadline.deadline_start.strftime("%H:%M:%S")

            data = {
                'day': day,
                'time': time,
            }

            return render(request, 'attribution/attribution_error_page_before.html', data)
        else:
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

def manual_attribution(request):
    return render(request, 'attribution/manual_attribution.html')