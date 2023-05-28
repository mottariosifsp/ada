from configuration.models import Criteria
from user.models import User
from attribution.models import TeacherQueuePosition
from django.shortcuts import render, redirect
import json

marcador = 0
tabela_data = ""

# Lógica para separar em áreas
# fazer filtro somente com os professores de uma determinada área

# Seleciona as áreas que o admin pertence
# def get_areas(request):
#         user = request.user
#         blocks = user.blocks.all()
#         areas = []
#         for block in blocks:
#             areas += block.areas.all()
#         # areas = [area for block in blocks for area in block.areas.all()] - colocar
#         return areas

# Seleciona o campo marcado pelo administrador e verifica qual é o atributo correspondente no histórico dos usuários
def get_selected_campo():
    if Criteria.objects.filter(is_select=True).exists():
        valor_numero = Criteria.objects.filter(is_select=True).values('number_criteria').first().get('number_criteria')
        print("Criterio escolhido pelo adm", valor_numero)
        campos = {
            1: 'birth',
            2: 'date_career',
            3: 'date_campus',
            4: 'date_professor',
            5: 'date_area',
            6: 'date_institute',
            # falta o 7
        }

        return campos.get(valor_numero, "campo")

# se nenhum critério foi selecionado para o adm retorna um campo em branco
    else:
        return ""

# metódo que adiciona os usuários na na fila (TeacherQueuePosition)
# vai ter algum problema quando tiver mais de uma fila para diferentes áreas ao memso tempo (como vai filtrar? 2 positions?)
def add_teacher_to_queue(teacher, position_input):
    position = position_input
    TeacherQueuePosition.objects.create(teacher=teacher, position=position)

# precisa remover professor também, caso ele saia da escola

# View que leva para a(s) fila(s) já definida pelo admin
def queue(request):
        campo = get_selected_campo()
        # #areas = get_areas(request)

        data = {
            'criterios': Criteria.objects.all(),
            'resultados': TeacherQueuePosition.objects.select_related('teacher').order_by('position').all(),
            'marcadorDiff': 0,
            'campo': campo,
            # #'areas': areas
        }

        # precisa fazer a lógica para ver filas diferentes

        print(1)

        return render(request, 'attribution/queue.html', {'data': data})

# View que leva para a página de definir a fila
def queueSetup(request):
    global marcador
    global tabela_data # variável utilizada caso a fila já tenha sido definida pelo menos uma vez pelo admin

    # if request.method == 'GET' and 'area' in request.GET:
    #     selected_area = request.GET.get('area')
    #     resultados = User.objects.filter(blocks__areas__name_area=selected_area)
    #     #areas = get_areas(request)
    #
    #     campo = get_selected_campo()
    #
    #     data = {
    #         'resultados': resultados,
    #         'marcadorDiff': 0,
    #         'campo': campo,
    #         #'areas': areas
    #     }
    #
    #     print("aqui22")
    #     return render(request, 'attribution/queueSetup.html', {'data': data})

    if request.method == 'POST': # adiciona os professores no model TeacherQueuePosition
        marcador = 1; # marcador fica como 1 para ter o controle que já foi criado uma tabela
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
            'marcadorDiff': 1, # serve para diferenciar se vai ser user (antes de enviar a tabela) ou teacher no html
            'campo': campo,
            # 'area': get_areas(request)
        }

        print(2)

        return render(request, 'attribution/queueSetup.html', {'data': data})

    else: # se a requisição não for POST e for GET sem ter passado a área, ou seja, sem ter atualização no filtro da área, vai cair aqui
        if marcador == 1:
            campo = get_selected_campo()

            users = User.objects.all()
            teacher_queue_users = TeacherQueuePosition.objects.values_list('teacher', flat=True)

            users_ausentes = [user for user in users if user.id not in teacher_queue_users]
            teacher_queue_users = teacher_queue_users
            teacher_queue_users.extend([user.id for user in users_ausentes])
            users_in_teacher_queue = User.objects.all()

            #areas = get_areas(request)

            #print(areas)

            data = {
                'resultados': users_in_teacher_queue,
                'marcadorDiff': 0,
                'campo': campo,
                #'areas': areas
            }

            print(3)

            return render(request, 'attribution/queueSetup.html', {'data': data})

        if Criteria.objects.filter(is_select=True).exists():
            campo = get_selected_campo()

            if campo != "":

                resultados = User.objects.all().order_by(f'history__{campo}')
                #areas = get_areas(request)

                #print(areas)

                data = {
                    'resultados': resultados,
                    'marcadorDiff': 0,
                    'campo': campo,
                    #'areas': areas
                }

                print(4)
                return render(request, 'attribution/queueSetup.html', {'data': data})
            else: # se o superadmin selecionou um critério que não tenha relação com nenhum atributo do histórico vai cair aqui

                resultados = User.objects.all()
                #validar por area
                data = {
                    'resultados': resultados,
                    'marcadorDiff': 0,
                    # 'campo': "Esse critério não corresponde a nenhum atributo do histórico do usuário"
                }
                return render(request, 'attribution/queueSetup.html', {'data': data})

        resultados = User.objects.all() # se nenhum critério foi selecionado pelo adm e não tiver feito nenhuma lista manual vai cair aqui
        campo = get_selected_campo()
        #areas = get_areas(request)

        data = {
            'resultados': resultados,
            'marcadorDiff': 0,
            'campo': campo,
            #'areas': areas
        }

        print(5)

        return render(request, 'attribution/queueSetup.html', {'data': data})
