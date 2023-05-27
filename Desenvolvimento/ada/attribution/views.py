from configuration.models import Criteria
from user.models import User
from attribution.models import TeacherQueuePosition
from django.shortcuts import render, redirect
# from django.http import JsonResponse
# from django.template.loader import render_to_string
# from django.template import RequestContext
import json
marcador = 0
tabela_data = ""

# Lógica para separar em áreas
# fazer filtro somente com os professores de uma determinada área

def get_areas(request):
    user = request.user  # precisa ser somente do admin - ok
    blocks = user.blocks.all()  # Obtém os blocos do usuário
    areas = []
    for block in blocks:
        areas += block.areas.all()

        return areas
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
            # rendered_table = render_to_string('attribution/queueSetup.html', {'data': data}, request=request)
            # print("rendered_table-AREA", rendered_table)
            # print("resultados-AREA", resultados)
                # rendered_table = render(request, 'attribution/queueSetup.html', {'data': data})
                # return JsonResponse({'rendered_table': rendered_table.content.decode('utf-8')})
            # return JsonResponse({'rendered_table': rendered_table})

        campo = get_selected_campo()
        areas = get_areas(request)

        data = {
            'criterios': Criteria.objects.all(),
            'resultados': TeacherQueuePosition.objects.select_related('teacher').order_by('position').all(),
            'marcadorDiff': 0,
            'campo': campo,
            'areas': areas
        }

        print(1)

        return render(request, 'attribution/queue.html', {'data': data})

def queueSetup(request):
    global marcador
    global tabela_data

    if request.method == 'GET':
        if 'area' in request.GET:
            selected_area = request.GET.get('area')
            # print("SELECTED-AREA", selected_area)
            resultados = User.objects.filter(blocks__areas__name_area=selected_area)
            # print("resultados-AREA-user-user", resultados)

            areas = get_areas(request)

            data = {
                'resultados': resultados,
                'marcadorDiff': 0,
                'areas': areas
            }

            # print("aqui")
            return render(request, 'attribution/queueSetup.html', {'data': data})

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

            areas = get_areas(request)

            print(areas)

            data = {
                'criterios': Criteria.objects.all(),
                'resultados': users_in_teacher_queue,
                'marcadorDiff': 0,
                'campo': campo,
                'areas': areas
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

                areas = get_areas(request)

                print(areas)
                    # Resto da lógica da view...

                # for user in resultados:
                #     blocks = user.blocks.all()
                #     for block in blocks:
                #         print(block.area)
                # for user in resultados:
                #     print(user.blocks)
                # resultados = TeacherQueuePosition.objects.all().order_by(f'teacher__history__{campo}')
                # print("Contents of resultados:", resultados)

                data = {
                    'criterios': Criteria.objects.all(),
                    'resultados': resultados,
                    'marcadorDiff': 0,
                    'campo': campo,
                    'areas': areas
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
