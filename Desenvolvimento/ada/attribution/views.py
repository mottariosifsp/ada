from configuration.models import Criteria
from user.models import User
from attribution.models import TeacherQueuePosition
from django.shortcuts import render, redirect
import json
marcador = 0
tabela_data = ""

# Lógica para separar em áreas
# fazer filtro somente com os professores de uma determinada área


def get_selected_campo():
    if Criteria.objects.filter(is_select=True).exists():
        criterion_selected = Criteria.objects.filter(is_select=True).values('number_criteria')
        valor_numero = criterion_selected[0]['number_criteria']

        campos = {
            1: 'birth',
            2: 'date_career',
            3: 'date_campus',
            4: 'date_professor',
            5: 'date_area',
            6: 'date_institute',
        }

        campo = campos.get(valor_numero)
        return campo

    else:
        campo = ""
        return campo

def add_teacher_to_queue(teacher, position_input):
    position = position_input
    TeacherQueuePosition.objects.create(teacher=teacher, position=position)

def queue(request):
    campo = get_selected_campo()

    data = {
        'criterios': Criteria.objects.all(),
        'resultados': TeacherQueuePosition.objects.select_related('teacher').order_by('position').all(),
        'marcadorDiff': 0,
        'campo': campo
    }

    print(1)

    return render(request, 'attribution/queue.html', {'data': data})

def queueSetup(request):
    global marcador
    global tabela_data

    if request.method == 'POST':
        marcador = 1;
        tabela_data = json.loads(request.POST['tabela_data'])

        campo = get_selected_campo()

        for professorInQueue in tabela_data:
            professor_registration_id = professorInQueue[1]
            position = professorInQueue[0]
            professor = User.objects.get(registration_id=professor_registration_id)

            if TeacherQueuePosition.objects.filter(teacher=professor).exists():
                TeacherQueuePosition.objects.filter(teacher=professor).update(position=position)
            else:
                add_teacher_to_queue(professor, position)

        data = {
            'resultados': TeacherQueuePosition.objects.select_related('teacher').order_by('position').all(),
            'marcadorDiff': 1,
            'campo': campo
        }

        print(2)

        return render(request, 'attribution/queueSetup.html', {'data': data})

    else:
        if marcador == 1:
            campo = get_selected_campo()

            users = User.objects.all()
            teacher_queue_users = TeacherQueuePosition.objects.values_list('teacher', flat=True)

            users_ausentes = [user for user in users if user.id not in teacher_queue_users]
            teacher_queue_users = list(teacher_queue_users)
            teacher_queue_users.extend([user.id for user in users_ausentes])
            users_in_teacher_queue = User.objects.all()

            data = {
                'criterios': Criteria.objects.all(),
                'resultados': users_in_teacher_queue,
                'marcadorDiff': 0,
                'campo': campo
            }

            print(3)

            return render(request, 'attribution/queueSetup.html', {'data': data})

        if Criteria.objects.filter(is_select=True).exists():
            campo = get_selected_campo()

            if campo != "":
                # na variável resultados será feito uma query, filtrando com o campo escolhido anteriormente, na variável campo
                # mostrando os resultados em ordem crescente
                # flat=True permite gerar um resultado em valores, retirando a estrutura de tupla dos dados (conceito de linha em
                # banco de dados), já que values_list retorna os valores em tupla
                # user = User.objects.get(id=1)
                # user_blocks = user.blocks.all()
                #
                # for block in user_blocks:
                #     print(block.name_block)

                resultados = User.objects.all().order_by(f'history__{campo}')

                for user in resultados:
                    blocks = user.blocks.all()
                    for block in blocks:
                        print(block.name_block)
                # for user in resultados:
                #     print(user.blocks)
                # resultados = TeacherQueuePosition.objects.all().order_by(f'teacher__history__{campo}')
                # print("Contents of resultados:", resultados)

                data = {
                    'criterios': Criteria.objects.all(),
                    'resultados': resultados,
                    'marcadorDiff': 0,
                    'campo': campo
                }

                print(4)
                return render(request, 'attribution/queueSetup.html', {'data': data})
            else:

                resultados = User.objects.all()
                #validar por area
                data = {
                    'criterios': Criteria.objects.all(),
                    'resultados': resultados,
                    'marcadorDiff': 0,
                    'campo': "Esse critério não corresponde a nenhum atributo do histórico do usuário"
                }
                return render(request, 'attribution/queueSetup.html', {'data': data})

        resultados = User.objects.all()

        data = {
            'criterios': Criteria.objects.all(),
            'resultados': resultados,
            'marcadorDiff': 0,
            'campo': "Nenhum critério foi selecionado"
        }

        print(5)

        return render(request, 'attribution/queueSetup.html', {'data': data})
