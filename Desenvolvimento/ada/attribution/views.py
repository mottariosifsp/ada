from area.models import Blockk
from attribution.task import schedule_task
from staff.models import Criteria, Deadline
from timetable.models import Timetable, Timetable_user
from user.models import User
from attribution.models import TeacherQueuePosition
from django.shortcuts import render, redirect
import json
from django.db.models import F, Sum, Value
from django.db import transaction
from django.utils import timezone
from datetime import datetime, timezone

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
    queue = TeacherQueuePosition.objects.filter(blockk=blockk).order_by('position').all()
    data = {
        'queue' : queue,
        'blockk': blockk
    }
    start_attribution(blockk)
    return render(request, 'attribution/attribution.html', data)

def start_attribution(blockk):
    queue = TeacherQueuePosition.objects.filter(blockk=blockk).order_by('position').all()
    for professor_in_queue in queue:
        print(professor_in_queue.teacher.first_name) 
        # attribution_process(blockk.timetable, professor_in_queue.teacher)

def attribution_process(timetable, professor):
    if validations(timetable, professor):
        assign_timetable_professor(timetable, professor)
        return True
    else:
        send_email(professor.email)   
        schedule_task(TEMPO_LIMITE_SEGUNDOS, professor)     

def send_email(professor_email):
    print("Email enviado")

def validations(timetable, professor):
    if timetable.user is None:
        return True
    # future validations

def assign_timetable_professor(timetable, professor):
    Timetable_user.objects.filter(timetable=timetable).update(user=professor)

def professor_to_end_queue(professor):

    size_queue = TeacherQueuePosition.objects.count()
    TeacherQueuePosition.objects.filter(teacher=professor).update(position=size_queue + 1)
    for professor_in_queue in TeacherQueuePosition.objects.all():
        professor_in_queue.position = F('position') - 1
        professor_in_queue.save()
        
