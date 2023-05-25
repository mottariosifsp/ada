from django.utils import timezone
from configuration.models import Criteria
from user.models import User, History
from django.shortcuts import render

timetoday = timezone.now()

def queueSetup(request):
    if (Criteria.objects.filter(is_select=True).exists()):
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
      
            resultados = User.objects.all().order_by(f'history__{campo}')

            data = {
                'resultados': resultados,
                'campo': campo
            }

            return render(request, 'attribution/queueSetup.html', {'data': data})
        else:

            resultados = User.objects.all()

            data = {
                'resultados': resultados,
                'campo': "Esse critério não corresponde a nenhum atributo do histórico do usuário"
            }
            return render(request, 'attribution/queueSetup.html', {'data': data})

    resultados = User.objects.all()

    data = {
        'resultados': resultados,
        'campo': "Nenhum critério foi selecionado"
    }

    return render(request, 'attribution/queueSetup.html', {'data': data})

