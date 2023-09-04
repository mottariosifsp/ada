from django.urls import path, include
from .views import home, profile, assignments, assignments_classs_list, show_assignment

urlpatterns = [
    path("", home, name="home_professor"),
    path("preferencia-atribuicao/", include("attribution_preference.urls")),
    path("perfil/", profile, name="profile"),
    path("atribuicoes/", assignments, name="assignments"),
    path("atribuicoes/<str:name_block>/", assignments_classs_list, name='assignments_classs_list'),
    path("ver/", show_assignment, name='show_assignment'),
]