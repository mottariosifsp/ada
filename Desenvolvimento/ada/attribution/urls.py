from django.urls import path
from attribution.views import queueSetup, queue, attribution, email_test

app_name = 'attribution'

urlpatterns = [
    path('queueSetup/', queueSetup, name='queueSetup'),
    path('queue/', queue, name='queue'),
    path('atribuicao-de-aulas/', attribution, name='attribution'),
    path('email_test/', email_test, name='email_test')
]