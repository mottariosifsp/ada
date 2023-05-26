from configuration.models import Criteria
from user.models import User, History
from attribution.models import TeacherQueuePosition
from django.shortcuts import render
import json
marcador = 0
tabela_data = ""


def add_teacher_to_queue(teacher, position_input):
    position = position_input
    TeacherQueuePosition.objects.create(teacher=teacher, position=position)


def queueSetup(request):
    global marcador
    global tabela_data

    if request.method == 'POST':
        marcador = 1;
        tabela_data = json.loads(request.POST['tabela_data'])

        print("Value of tabela_data:", tabela_data)
        # print("Contents of request.POST:", request.POST)

        tabela_data = json.loads(request.POST['tabela_data'])

        for professorInQueue in tabela_data:
            professor_registration_id = professorInQueue[1]
            position = professorInQueue[0]
            professor = User.objects.get(registration_id=professor_registration_id)
            # professor = User.objects.get(id=registration_id)
            # professor = User.objects.get(registration_id=registration_id)

            # try:
            #     professor = User.objects.get(id=registration_id)
            # except User.DoesNotExist:
            #     print("Professor not found:", registration_id)
            #     continue

            print("Professor: ", professor)

            if TeacherQueuePosition.objects.filter(teacher=professor).exists():
                TeacherQueuePosition.objects.filter(teacher=professor).update(position=position)
            else:
                add_teacher_to_queue(professor, position)

        data = {
            'criterios': Criteria.objects.all(),
            'resultados': TeacherQueuePosition.objects.select_related('teacher').order_by('position').all(), #nao vai ser mais o user, ver como arrumar
            'campo': "mudado manualmente"
        }

        return render(request, 'attribution/queueSetup.html', {'data': data})

    else:
        if marcador == 1:
            data = {
                'criterios': Criteria.objects.all(),
                'resultados': TeacherQueuePosition.objects.select_related('teacher').order_by('position').all(),#nao vai ser mais o user, ver como arrumar
                'campo': "mudado manualmente"
            }

            return render(request, 'attribution/queueSetup.html', {'data': data})

        if Criteria.objects.filter(is_select=True).exists():
            criterion_selected = Criteria.objects.filter(is_select=True).values('number_criteria')
            valor_numero = criterion_selected[0]['number_criteria'] #juntar

            campos = {
                1: 'birth',
                2: 'date_career',
                3: 'date_campus',
                4: 'date_professor',
                5: 'date_area',
                6: 'date_institute',
            }

            campo = campos.get(valor_numero)

            if campo:
                # na variável resultados será feito uma query, filtrando com o campo escolhido anteriormente, na variável campo
                # mostrando os resultados em ordem crescente
                # flat=True permite gerar um resultado em valores, retirando a estrutura de tupla dos dados (conceito de linha em
                # banco de dados), já que values_list retorna os valores em tupla

                # resultados = User.objects.all().order_by(f'history__{campo}')
                # campo = 'birth'


                resultados = TeacherQueuePosition.objects.all().order_by(f'teacher__history__{campo}')
                print("Contents of resultados:", resultados)

                # resultados = TeacherQueuePosition.objects.all().order_by(f'history__{campo}')

                data = {
                    'criterios': Criteria.objects.all(),
                    'resultados': resultados,
                    'campo': campo
                }

                return render(request, 'attribution/queueSetup.html', {'data': data})
            else:

                resultados = User.objects.all()
                #validar
                data = {
                    'criterios': Criteria.objects.all(),
                    'resultados': resultados,
                    'campo': "Esse critério não corresponde a nenhum atributo do histórico do usuário"
                }
                return render(request, 'attribution/queueSetup.html', {'data': data})

        resultados = User.objects.all()

        data = {
            'criterios': Criteria.objects.all(),
            'resultados': resultados,
            'campo': "Nenhum critério foi selecionado"
        }

        return render(request, 'attribution/queueSetup.html', {'data': data})

