from django.urls import path

from .views import attributionConfiguration, confirmConfiguration, showActualDeadline

urlpatterns = [
    path("", attributionConfiguration, name="attributionConfiguration"),
    path("prazo-cadastrado/", confirmConfiguration, name="confirmConfiguration"),
    path("prazo-atual/", showActualDeadline, name="showActualDeadline")
]