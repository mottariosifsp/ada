from django.urls import path
from .views import home, confirm_deadline_configuration, show_current_deadline, deadline_configuration, professors_list

urlpatterns = [
    path("", home, name="home"),
    path("cadastrar-prazos/", deadline_configuration, name="deadline_configuration"),
    path("prazo-cadastrado/", confirm_deadline_configuration, name="confirm_deadline_configuration"),
    path("prazo-atual/", show_current_deadline, name="show_current_deadline"),
    path("professors-list/", professors_list, name="professors_list"),
]