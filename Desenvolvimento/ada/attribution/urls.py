from django.urls import path
from attribution.views import queueSetup, queue, attribution

app_name = 'attribution'

urlpatterns = [
    path('queueSetup/', queueSetup, name='queueSetup'),
    path('queue/', queue, name='queue'),
    path('atribuicao-de-aulas/', attribution, name='attribution')
]