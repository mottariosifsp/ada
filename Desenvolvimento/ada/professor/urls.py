from django.urls import path, include
from .views import home

urlpatterns = [
    path("", home, name="home"),
    path("preferencia-atribuicao/", include("attribution_preference.urls"))
]