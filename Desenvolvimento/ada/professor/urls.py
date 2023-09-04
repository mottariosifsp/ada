from django.urls import path, include
from .views import home, profile, assignments, final_assignments_classs, show_assignment

urlpatterns = [
    path("", home, name="home_professor"),
    path("preferencia-atribuicao/", include("attribution_preference.urls")),
    path("perfil/", profile, name="profile"),
    path("atribuicoes/", assignments, name="assignments"),
    path("atribuicoes/<str:name_block>/", final_assignments_classs, name='final_assignments_classs'),
    path("ver/", show_assignment, name='show_assignment'),
]