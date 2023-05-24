from django.utils import timezone
from configuration.models import Criteria
from user.models import User, History
from django.shortcuts import render

timetoday = timezone.now()

def queue_based_on_criterion(request):
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
            resultados = History.objects.values_list(campo, flat=True).order_by(f'{campo}')
            valores = [valor.strftime('%Y-%m-%d') for valor in resultados]
            valores_formatados = ', '.join(valores) # join concatena os valores

            return render(request, 'attribution/fila.html', {'resultados': valores_formatados, 'avaliado': campo})
        else:
            resultados = History.objects.none()  # retorna uma query vazia se o campo não for válido
            return render(request, 'attribution/fila.html', {'resultados': resultados})

    else:
        criterion_selected = 'Nenhum critério foi selecionado para formar a fila'
        return render(request, 'attribution/fila.html', {'resultados': criterion_selected})

