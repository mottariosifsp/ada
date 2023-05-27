from django.urls import path

from .views import attributionConfiguration, confirmConfiguration 

urlpatterns = [
    path("", attributionConfiguration, name="attributionConfiguration"),
    path("prazo-cadastrado/", confirmConfiguration, name="confirmConfiguration")
]