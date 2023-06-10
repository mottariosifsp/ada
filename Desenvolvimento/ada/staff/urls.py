from django.urls import path
from .views import attribution_configuration, attribution_configuration_confirm, class_create, class_delete, \
    classes_list, classes_list_saved, create_timetable, show_timetable, home, confirm_deadline_configuration, \
    show_current_deadline, deadline_configuration, professors_list, timetables, update_save, blocks_list, block_detail, \
    course_update_save, course_delete, course_create, queue_create, queue_show

urlpatterns = [
    path("", home, name="home_staff"),
    path("prazo/cadastrar/", deadline_configuration, name="deadline_configuration"),
    path("prazo/alteracoes-salvas/", confirm_deadline_configuration, name="confirm_deadline_configuration"),
    path("prazo/atual/", show_current_deadline, name="show_current_deadline"),
    path("professores/", professors_list, name="professors_list"),
    path("alteracoes-salvas/", update_save, name="update_save"),
    path("turmas/", classes_list, name="classes_list"),
    path("turmas/alteracoes-salvas/", classes_list_saved, name="classes_list_saved"),
    path("turmas/cadastrar/", class_create, name="class_create"),
    path("turmas/deletar/", class_delete, name="class_delete"),
    path("blocos/", blocks_list, name="blocks_list"),
    path("detalhes-bloco/<str:registration_block_id>/", block_detail, name="block_detail"),
    path("detalhes-bloco/atualizar-bloco", course_update_save, name="course_update_save"),
    path("detalhes-bloco/criar-materia", course_create, name="course_create"),
    path("detalhes-bloco/deletar-materia", course_delete, name="course_delete"),
    path("detalhes-bloco/criar-fila", queue_create, name="queue_create"),
    path("detalhes-bloco/lista", queue_show, name="queue_show"),
    path("grade/cadastrar/", create_timetable, name="create_timetable"),
    path("grade/ver/", show_timetable, name="show_timetable"),
    path("grade/", timetables, name="timetables"),
    path("atribuicao/configuracao/", attribution_configuration, name="attribution_configuration"),
    path("atribuicao/confirmar/", attribution_configuration_confirm, name="attribution_configuration_confirm")
]