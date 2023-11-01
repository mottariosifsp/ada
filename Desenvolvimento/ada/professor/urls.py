from django.urls import path, include
from .views import home, profile, assignments, assignments_classs_list, show_assignment, professor_blocks_list, \
    professor_block_detail, privacy_policy, terms_and_conditions, contact, about

urlpatterns = [
    path("", home, name="home_professor"),
    path("preferencia-atribuicao/", include("attribution_preference.urls")),
    path("perfil/", profile, name="profile"),
    path("atribuicoes/", assignments, name="assignments"),
    path("atribuicoes/<str:name_block>/", assignments_classs_list, name='assignments_classs_list'),
    path("ver-atribuicoes/", show_assignment, name='show_assignment'),
    path("blocos/", professor_blocks_list, name="professor_blocks_list"),
    path("detalhes-bloco/<str:registration_block_id>/", professor_block_detail, name="professor_block_detail"),
    path("politica-de-privacidade/", privacy_policy, name="privacy_policy"),
    path("termos-e-condições-de-uso/", terms_and_conditions, name="terms_and_conditions"),
    path("contato", contact, name="contact"),
    path("sobre", about, name="about")
]
# gource