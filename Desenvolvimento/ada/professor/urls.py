from django.urls import path, include
from .views import home, profile, assignments

urlpatterns = [
    path("", home, name="home_professor"),
    path("preferencia-atribuicao/", include("attribution_preference.urls")),
    path("perfil/", profile, name="profile"),
    path("atribuicoes/", assignments, name="assignments"),
]