from django.urls import path
from .views import classes_list, classes_list_saved, home, confirm_deadline_configuration, show_current_deadline, deadline_configuration, professors_list, update_save, blocks_list, block_detail, course_update_save


urlpatterns = [
    path("", home, name="home"),
    path("cadastrar-prazos/", deadline_configuration, name="deadline_configuration"),
    path("prazo-cadastrado/", confirm_deadline_configuration, name="confirm_deadline_configuration"),
    path("prazo-atual/", show_current_deadline, name="show_current_deadline"),
    path("professores/", professors_list, name="professors_list"),
    path("alteracoes-salvas/", update_save, name="update_save"),
    path("turmas/", classes_list, name="classes_list"),
    path("turmas/salvas/", classes_list_saved, name="classes_list_saved"),
    path("blocos/", blocks_list, name="blocks_list"),
    path("detalhes-bloco/<str:registration_block_id>/", block_detail, name="block_detail"),
    path("detalhes-bloco/atualizar-bloco", course_update_save, name="course_update_save"),
]