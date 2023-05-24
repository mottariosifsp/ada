from django.utils import timezone
from configuration.models import Criteria
from django.core.exceptions import ValidationError
from django.shortcuts import render

timetoday = timezone.now()

def queue_based_on_criterion(request):
    if (Criteria.objects.filter(is_select=True).exists()):
        criteria_select = Criteria.objects.filter(is_select=True).values('number_criteria')
        return render(request, 'attribution/fila.html', {'criteria_select': criteria_select})
    else:
        criteria_select = 'Nenhum critério foi selecionado para formar a fila'
        return render(request, 'attribution/fila.html', {'criteria_select': criteria_select})


# Create your views here.
