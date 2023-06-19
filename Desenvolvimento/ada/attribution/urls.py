from django.urls import path
from attribution.views import attribution, email_test, manual_attribution, attribution_detail, attribution_list

app_name = 'attribution'

urlpatterns = [
    path('atribuicao-de-aulas/', attribution, name='attribution'),
    path('atribuicao-manual/', manual_attribution, name='manual_attribution'),
    path('email_test/', email_test, name='email_test'),
    path("atribuicao-blocos/<str:registration_block_id>/", attribution_detail, name="attribution_detail"),
    path("atribuicao-blocos/", attribution_list, name="attribution_list"),
]