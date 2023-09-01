from django.urls import path
from .views import attribution_configuration, attribution_configuration_confirm, attribution_configuration_index, class_create, class_delete, classes_list, classes_list_saved, create_timetable, edit_timetable, show_timetable, home,\
    show_current_deadline, professors_list, timetables, update_save, blocks_list, block_detail, course_update_save, course_delete, course_create, queue_create, queue_show, add_new_professor

urlpatterns = [
    path("", home, name="home_staff"),
    path("prazo/atual/", show_current_deadline, name="show_current_deadline"),
    path("professores/", professors_list, name="professors_list"),
    path("professor-adiciondo/", add_new_professor, name="add_new_professor"),
    path("alteracoes-salvas/", update_save, name="update_save"),
    path("turmas/", classes_list, name="classes_list"),
    path("turmas/alteracoes-salvas/", classes_list_saved, name="classes_list_saved"),
    path("turmas/cadastrar/", class_create, name="class_create"),
    path("turmas/deletar/", class_delete, name="class_delete"),
    path("blocos/", blocks_list, name="blocks_list"),
    path("detalhes-bloco/<str:registration_block_id>/", block_detail, name="block_detail"),
    path("detalhes-bloco/atualizar-bloco", course_update_save, name="course_update_save"),
    path("detalhes-bloco/criar-materia", course_create, name="course_create"),
    path("detalhes-bloco/deletar-materia", course_delete, name="course_delete"), # trocar por disciplina
    path("detalhes-bloco/criar-fila", queue_create, name="queue_create"),
    path("detalhes-bloco/lista", queue_show, name="queue_show"),
    path("grade/cadastrar/", create_timetable, name="create_timetable"),
    path("grade/editar/", edit_timetable, name="edit_timetable"),
    path("grade/ver/", show_timetable, name="show_timetable"),
    path("grade/", timetables, name="timetables"),
    path("atribuicao/configuracao/", attribution_configuration, name="attribution_configuration"),
    path("atribuicao/confirmar/", attribution_configuration_confirm, name="attribution_configuration_confirm"),
    path("atribuicao/", attribution_configuration_index, name="attribution_configuration_index")
]