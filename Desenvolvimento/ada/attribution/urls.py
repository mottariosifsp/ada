from django.urls import path
from attribution.views import attribution, email_test

app_name = 'attribution'

urlpatterns = [
    path('atribuicao-de-aulas/', attribution, name='attribution'),
    path('email_test/', email_test, name='email_test')
]