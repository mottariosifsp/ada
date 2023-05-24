from django.db.models import Q
from django.utils import timezone
from configuration.models import Criteria
from user.models import User, History
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.shortcuts import render

timetoday = timezone.now()

def queue_based_on_criterion(request):
    if (Criteria.objects.filter(is_select=True).exists()):
        #criterion_selected = Criteria.objects.filter(is_select=True).values('number_criteria')
        #user_filter = User.objects.filter().values('number_criteria')

        campos = {
            1: 'birth',
            2: 'date_career',
            3: 'date_campus',
            4: 'date_professor',
            5: 'date_area',
            6: 'date_institute'
        }

        campo = campos.get(2)

        if campo:
            #filtro = Q(**{campo: None})
            filtro = Q(**{campos.get(2): campo})
            resultados = History.objects.filter(filtro)
            return render(request, 'attribution/fila.html', {'resultados': resultados})
        else:
            resultados = History.objects.none()  # Retornar uma queryset vazia se o campo não for válido
            return render(request, 'attribution/fila.html', {'resultados': resultados})

    else:
        criterion_selected = 'Nenhum critério foi selecionado para formar a fila'
        return render(request, 'attribution/fila.html', {'criterion_selected': criterion_selected})




# Create your views here.
