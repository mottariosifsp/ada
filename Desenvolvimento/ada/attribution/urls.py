from django.urls import path
from attribution.views import attribution, email_test, manual_attribution

app_name = 'attribution'

urlpatterns = [
    path('atribuicao-de-aulas/', attribution, name='attribution'),
    path('atribuicao-manual/', manual_attribution, name='manual_attribution'),
    path('email_test/', email_test, name='email_test')
]