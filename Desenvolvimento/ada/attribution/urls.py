from django.urls import path
from attribution.views import attribution, email_test, manual_attribution, manual_attribution_confirm, manual_attribution_timesup

app_name = 'attribution'

urlpatterns = [
    path('atribuicao-de-aulas/', attribution, name='attribution'),
    path('atribuicao-manual/', manual_attribution, name='manual_attribution'),
    path('email_test/', email_test, name='email_test'),
    path('atribuicao-manual-confirmar/', manual_attribution_confirm, name='manual_attribution_confirm'),
    path('atribuicao-manual-erro/', manual_attribution_timesup, name='manual_attribution_timesup'),
    # path("atribuicao-blocos/<str:registration_block_id>/", attribution_detail, name="attribution_detail"),
]