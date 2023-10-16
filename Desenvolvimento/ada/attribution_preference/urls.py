from django.urls import path
from .views import attribution_preference, courses_attribution_preference, disponibility_attribution_preference, show_attribution_preference
# gource
urlpatterns = [
    path('editar-disponibilidade/', disponibility_attribution_preference, name='disponibility_attribution_preference'),
    path('editar-cursos/', courses_attribution_preference, name='courses_attribution_preference'),
    path('mostrar/<str:year>', show_attribution_preference, name='show_attribution_preference'),
    path('', attribution_preference, name='attribution_preference'),
]