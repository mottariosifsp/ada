from django.urls import path
from .views import attribution_preference, courses_attribution_preference, disponibility_attribution_preference, show_attribution_preference

urlpatterns = [
    path('editar-disponibilidade/<str:registration_block_id>/', disponibility_attribution_preference, name='disponibility_attribution_preference'),
    path('editar-cursos/<str:registration_block_id>/', courses_attribution_preference, name='courses_attribution_preference'),
    path('mostrar/<str:registration_block_id>/', show_attribution_preference, name='show_attribution_preference'),
    path('', attribution_preference, name='attribution_preference'),
]