from django.urls import path, include
from .views import home, profile, assignments, final_assignments_classs

urlpatterns = [
    path("", home, name="home_professor"),
    path("preferencia-atribuicao/", include("attribution_preference.urls")),
    path("perfil/", profile, name="profile"),
    path("atribuicoes/", assignments, name="assignments"),
    path("atribuicoes/<str:area_name>/", final_assignments_classs, name="final_assignments_classs"),
]