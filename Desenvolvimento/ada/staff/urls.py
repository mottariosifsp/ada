from django.urls import path
from .views import classes_list, home, confirm_deadline_configuration, show_current_deadline, deadline_configuration, professors_list, update_save

urlpatterns = [
    path("", home, name="home"),
    path("cadastrar-prazos/", deadline_configuration, name="deadline_configuration"),
    path("prazo-cadastrado/", confirm_deadline_configuration, name="confirm_deadline_configuration"),
    path("prazo-atual/", show_current_deadline, name="show_current_deadline"),
    path("professores/", professors_list, name="professors_list"),
    path("alteracoes-salvas/", update_save, name="update_save"),
    path("turmas/", classes_list, name="classes_list"),
]