from django.urls import path
from .views import attribution_preference, courses_attribution_preference ,confirm_attribution_preference

urlpatterns = [
    path('criar-fpa/editar-disponibilidade/', attribution_preference, name='attribution_preference'),
    path('criar-fpa/editar-cursos/', courses_attribution_preference, name='courses_attribution_preference'),
    path('salvar-fpa/', confirm_attribution_preference, name='confirm_attribution_preference'),
]