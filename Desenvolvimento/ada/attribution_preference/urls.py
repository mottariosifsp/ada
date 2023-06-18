from django.urls import path
from .views import attribution_preference, courses_attribution_preference ,disponibility_attribution_preference

urlpatterns = [
    path('criar-fpa/editar-disponibilidade/', disponibility_attribution_preference, name='disponibility_attribution_preference'),
    path('criar-fpa/editar-cursos/', courses_attribution_preference, name='courses_attribution_preference'),
    path('', attribution_preference, name='attribution_preference'),
]