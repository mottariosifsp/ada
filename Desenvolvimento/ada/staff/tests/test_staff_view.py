import pytest
import json
from datetime import datetime, timedelta
from user.models import User, History, AcademicDegree
from django.contrib.auth import get_user_model
from django.urls import reverse
from area.models import Blockk, Area
from enum import Enum
from staff.models import Deadline, Criteria
from staff.views import attribution_configuration_confirm, create_timetable, edit_timetable, save_combo_day, \
    timetable_combo_saver, get_selected_field, calculate_total_score, queue_create
import time
from unittest.mock import patch
from django.test import RequestFactory
from django.utils import timezone
from classs.models import Classs
from course.models import Course
from timetable.models import Timetable, Day_combo, Timeslot
from django.urls import resolve
from django.db import transaction
import factory  # cria vários registros fictícios automaticamente
from django.db.models import Sum
from datetime import date
from pytest_django.asserts import assertRedirects
from attribution.models import TeacherQueuePosition, TeacherQueuePositionBackup
from django.test import Client
from mixer.backend.django import mixer


@pytest.fixture
def user():
    return get_user_model().objects.create_user(
        first_name='Joao',
        email='joao@email.com',
        password='password',
        is_staff=True
    )


# Usuário precisa estar logado para não ser uma requição 302 (redirect)
@pytest.fixture
def client_logged_in(user, client):
    user_instance = User.objects.create(
        registration_id='sp1111111',
        first_name='Albert',
        email='einstein @email.com',
        cell_phone='1234567890'
    )
    user_instance.set_password('testpass')
    user_instance.is_staff = True  # Defina as permissões de staff conforme necessário
    user_instance.save()

    client.login(username=user_instance.registration_id, password='testpass')
    return client


@pytest.fixture
def blockk():
    return Blockk.objects.create(registration_block_id=1)


@pytest.fixture
def deadlines(blockk):
    now = datetime.now()
    startFPADeadline = now + timedelta(days=1)
    endFPADeadline = now + timedelta(days=2)
    startAssignmentDeadline = now + timedelta(days=3)
    endAssignmentDeadline = now + timedelta(days=4)

    return Deadline.objects.create(
        name='Test Deadline',
        deadline_start=startFPADeadline,
        deadline_end=endFPADeadline,
        blockk=blockk
    )


# Teste para confirmar a configuração de atribuição após o envio de dados de configuração
@pytest.mark.django_db
def test_attribution_configuration_confirm(client_logged_in, blockk, deadlines):
    # Obtém a URL da view 'attribution_configuration_confirm'
    url = reverse('attribution_configuration_confirm')

    # Envia uma solicitação POST com dados simulados de configuração
    response = client_logged_in.post(url, {
        'blockk': blockk.registration_block_id,
        'startFPADeadline': deadlines.deadline_start.strftime("%Y-%m-%dT%H:%M"),
        'endFPADeadline': deadlines.deadline_end.strftime("%Y-%m-%dT%H:%M"),
        'startAssignmentDeadline': deadlines.deadline_start.strftime("%Y-%m-%dT%H:%M"),
        'endAssignmentDeadline': deadlines.deadline_end.strftime("%Y-%m-%dT%H:%M")
    })

    #  Confirma se a resposta tem um código de status HTTP 200 (OK)
    assert response.status_code == 200


@pytest.fixture
def user(client):
    User = get_user_model()
    user = User.objects.create_user(registration_id='123', password='password', email="renato@email.com", is_staff=True)
    client.login(registration_id='123', password='password')
    return user


# Teste para atualização e salvamento com histórico existente
@pytest.mark.django_db
def test_update_save_with_existing_history(user, client):
    # Cria um objeto de histórico
    history = History.objects.create(
        birth='1990-01-01',
        date_career='2020-01-01',
        date_campus='2021-01-01',
        date_professor='2022-01-01',
        date_area='2023-01-01',
        date_institute='2024-01-01'
    )

    # Associa o objeto de histórico ao usuário e o salva
    user.history = history
    user.save()

    # Dados para atualização
    data = {
        'registration_id': '123',
        'birth': '1990-01-01',
        'date_career': '2020-01-01',
        'date_campus': '2021-01-01',
        'date_professor': '2022-01-01',
        'date_area': '2023-01-01',
        'date_institute': '2024-01-01',
        'academic_degrees': json.dumps([{'name': 'PhD', 'punctuation': 4.0}]),
    }

    # Envia uma solicitação POST para atualização
    response = client.post(reverse('update_save'), data=data)

    # Verificações
    assert response.status_code == 200  # Verifica se a atualização foi bem-sucedida
    assert history.academic_degrees.count() == 1  # Verifica se um grau acadêmico foi associado ao histórico


# Teste para atualização e salvamento sem histórico existente
@pytest.mark.django_db
def test_update_save_without_existing_history(user, client):
    # Dados para atualização
    data = {
        'registration_id': '123',
        'birth': '1990-01-01',
        'date_career': '2020-01-01',
        'date_campus': '2021-01-01',
        'date_professor': '2022-01-01',
        'date_area': '2023-01-01',
        'date_institute': '2024-01-01',
        'academic_degrees': json.dumps([{'name': 'PhD', 'punctuation': 4.0}]),
    }

    # Envia uma solicitação POST para atualização
    response = client.post(reverse('update_save'), data=data)

    # Verificações
    assert response.status_code == 200  # Verifica se a atualização foi bem-sucedida
    user.refresh_from_db()  # Atualiza a instância do usuário para obter o histórico atualizado
    assert user.history is not None  # Verifica se um novo histórico foi criado


# Teste para atualização e limpeza
@pytest.mark.django_db
def test_update_save_cleanup(user, client):
    # Cria um grau acadêmico
    academic_degree = AcademicDegree.objects.create(name='MSc', punctuation=3.5)

    # Dados para atualização com limpeza de graus acadêmicos
    data = {
        'registration_id': '123',
        'birth': '1990-01-01',
        'date_career': '2020-01-01',
        'date_campus': '2021-01-01',
        'date_professor': '2022-01-01',
        'date_area': '2023-01-01',
        'date_institute': '2024-01-01',
        'academic_degrees': '[]',  # Lista vazia indica limpeza
    }

    # Envia uma solicitação POST para atualização
    response = client.post(reverse('update_save'), data=data)

    # Verificações
    assert response.status_code == 200  # Verifica se a atualização foi bem-sucedida
    assert not AcademicDegree.objects.filter(
        pk=academic_degree.pk).exists()  # Verifica se o grau acadêmico foi removido


# Teste para atualização e salvamento sem acesso de usuário
@pytest.mark.django_db
def test_update_save_no_access(client):
    # Cria um usuário não administrativo
    User = get_user_model()
    user = User.objects.create_user(registration_id='456', email="marcos@email.com", password='password',
                                    is_staff=False)

    # Realiza o login como o usuário criado
    client.login(registration_id='456', password='password')

    # Dados para atualização com limpeza de graus acadêmicos
    data = {
        'registration_id': '456',
        'birth': '1990-01-01',
        'date_career': '2020-01-01',
        'date_campus': '2021-01-01',
        'date_professor': '2022-01-01',
        'date_area': '2023-01-01',
        'date_institute': '2024-01-01',
        'academic_degrees': '[]',
    }

    # Envia uma solicitação POST para atualização
    response = client.post(reverse('update_save'), data=data)

    # Verificações
    assert response.status_code == 302  # Deveria haver um redirecionamento para a página de login


@pytest.fixture
def area():
    return Area.objects.create(
        registration_area_id='area-1',
        name_area='Area 1',
        acronym='A1',
        exchange_area=True,
        is_high_school=True
    )


# Teste para listar classes de usuário
@pytest.mark.django_db
def test_classes_list(user, client):
    # Obtém a resposta ao acessar a página de listagem de classes
    response = client.get(reverse('classes_list'))

    # Verifica se a resposta tem um código de status HTTP 200 (OK)
    assert response.status_code == 200  # Deve indicar que a listagem de classes foi carregada com sucesso


# Erro na view!! - TODO
# @pytest.mark.django_db
# def test_classes_list_saved_post_existing_class(user, area, client):
#     classs = Classs.objects.create(registration_class_id='class-123', period='MORNING', semester=1, area=area)
#
#     data = {
#         'registration_class_id': 'class-123',
#         'period': enum.Period.afternoon.value,  # Use the correct choice value from enum.Period
#         'semester': 2,
#         'area': area.id,
#     }
#
#     response = client.post(reverse('classes_list_saved'), data=data, content_type='application/json')
#     assert response.status_code == 200
#
#     classs.refresh_from_db()
#     assert classs.period == enum.Period.afternoon.value  # Verify if the period value is updated
#     assert classs.semester == 2
#     assert classs.area == area

# Provável erro na view - TODO
# @pytest.mark.django_db
# def test_classes_list_saved_post_new_class(user, area, client):
#     data = {
#         'registration_class_id': 'class-123',
#         'period': enum.Period.morning.value,
#         'semester': 1,
#         'area': area.id,
#     }
#
#     response = client.post(reverse('classes_list_saved'), data=data, content_type='application/json')
#     assert response.status_code == 200
#
#     classs = Classs.objects.get(registration_class_id='class-123')
#     assert classs.period == enum.Period.morning.value
#     assert classs.semester == 1
#     assert classs.area == area


# Erro na view
# @pytest.mark.django_db
# def test_class_create(user, area, client):
#     data = {
#         'registration_class_id': 'class-123',
#         'period': enum.Period.morning.value,
#         'semester': 1,
#         'area': area.id,
#     }
#
#     response = client.post(reverse('class_create'), data=data, content_type='application/json')
#     assert response.status_code == 200  # Change this to the expected status code, e.g., 201
#
#     classs = Classs.objects.get(registration_class_id='class-123')
#     assert classs.period == enum.Period.morning.value
#     assert classs.semester == 1
#     assert classs.area == area

# Test for class_delete view
# Erro na view
# @pytest.mark.django_db
# def test_class_delete(user, area, classs, client):
#     response = client.post(reverse('class_delete'), data={'id': classs.id}, content_type='application/json')
#     assert response.status_code == 200
#
#     with pytest.raises(Classs.DoesNotExist):
#         Classs.objects.get(id=classs.id)

# @pytest.fixture
# def blockk():
#     return Blockk.objects.create(
#         registration_block_id='block-123',
#         name_block='Test Block',
#         area=area
#     )

# Resolver - TODO
# Test for course_create view

# User = get_user_model()
#
#
# @pytest.fixture
# def user():
#     return User.objects.create_user(
#         first_name='Joao',
#         email='joao@email.com',
#         password='testpass',
#         is_staff=True
#     )
#
# fake = Faker()
#
# @pytest.fixture
# def area_and_block_instances(django_db_setup):
#     block_instance = Blockk.objects.create(
#         registration_block_id='block-123',
#         name_block='Test Block',
#         acronym='TB'
#     )
#
#     area_instance = Area.objects.create(
#         registration_area_id='area-123',
#         name_area='Test Area',
#         acronym='TA',
#         exchange_area=True,
#         is_high_school=True
#     )
#     area_instance.blocks.add(block_instance)
#
#     return area_instance, block_instance
#
#
# @pytest.mark.django_db
# def test_course_create(user, area_instance, block_instance, client):
#     data = {
#         'registration_course_id': 'course-123',
#         'name_course': 'Test Course',
#         'acronym': 'TC',
#         'areaId': area_instance.id,
#         'blockId': block_instance.id,
#     }
#
#     response = client.post(reverse('course_create'), data=data, content_type='application/json')
#     assert response.status_code == 200  # Change this to the expected status code, e.g., 201
#
#     course_count = Course.objects.filter(registration_course_id='course-123').count()
#     assert course_count == 1
#
#     course = Course.objects.get(registration_course_id='course-123')
#     assert course.name_course == 'Test Course'
#     assert course.acronym == 'TC'
#     assert course.area == area_instance
#     assert course.blockk == block_instance

@pytest.fixture
def block_instance(django_db_setup):
    return Blockk.objects.create(
        registration_block_id='block-123',
        name_block='Test Block',
        acronym='TB',
    )


@pytest.fixture
def area_instance(django_db_setup, block_instance):
    return Area.objects.create(
        registration_area_id='area-123',
        name_area='Test Area',
        acronym='TA',
        exchange_area=True,
        is_high_school=True
    )


@pytest.fixture
def class_instance(django_db_setup, area_instance):
    return Classs.objects.create(
        registration_class_id='class-123',
        period='MORNING',
        semester=1,
        area=area_instance
    )


# @pytest.fixture
# def timetable_instance(django_db_setup, class_instance):
#     return Timetable.objects.create(
#         classs=class_instance,
#         day='Monday',
#         start_time='08:00',
#         end_time='10:00'
#     )
#
#
# @pytest.fixture
# def timetable_instance(django_db_setup, class_instance):
#     return Timetable.objects.create(classs=class_instance)
#
# @pytest.fixture
# def timeslot_instance(django_db_setup):
#     return Timeslot.objects.create(hour_start='08:00', hour_end='10:00')
#

class Day(Enum):
    monday = 'MONDAY'
    tuesday = 'TUESDAY'
    wednesday = 'WEDNESDAY'
    thursday = 'THURSDAY'
    friday = 'FRIDAY'
    saturday = 'SATURDAY'


@pytest.fixture
def day_combo_instance(django_db_setup, timeslot_instance):
    return Day_combo.objects.create(day=Day.monday.value)


#
# @pytest.fixture
# def timetable_user_instance(django_db_setup, timetable_instance, user):
#     return Timetable_user.objects.create(timetable=timetable_instance, user=user)
#
#
# @pytest.mark.django_db
# def test_timetables_view(user, block_instance, area_instance, class_instance, timetable_instance, client):
#     client.force_login(user)
#     url = reverse('timetables')
#
#     response = client.get(url)
#     assert response.status_code == 200
#
#     assert 'timetables' in response.context
#     assert 'user_blocks' in response.context
#     assert 'classes' in response.context


# @pytest.fixture
# def class_instance(django_db_setup):
#     return Classs.objects.create(
#         registration_class_id='class-123',
#         period='MORNING',
#         semester=1,
#         area_id=1
#     )

@pytest.fixture
def course_instance(django_db_setup, area_instance, block_instance):
    return Course.objects.create(
        registration_course_id='course-123',
        name_course='Test Course',
        acronym='TC',
        area=area_instance,
        blockk=block_instance
    )


@pytest.fixture
def timeslot_instance(django_db_setup):
    return Timeslot.objects.create(
        position=1,
        hour_start='08:00:00',
        hour_end='10:00:00'
    )


#
# Teste para renderizar a página de criação de nova grade horária
@pytest.mark.django_db
def test_create_timetable_get_new_timetable_render(user, class_instance, client):
    response = client.get(reverse('create_timetable'), {'class': class_instance.registration_class_id})
    assert response.status_code == 200  # Deve carregar a página com sucesso
    assert 'timeslots' in response.context  # Deve conter os timeslots no contexto
    assert 'classs' in response.context  # Deve conter as classes no contexto
    assert 'courses' in response.context  # Deve conter os cursos no contexto


# Teste para redirecionar para a página de edição se já existir uma grade horária
@pytest.mark.django_db
def test_create_timetable_get_existing_timetable_redirect(user, class_instance, client):
    timetable = Timetable.objects.create(classs=class_instance)
    url = reverse('create_timetable') + f'?class={class_instance.registration_class_id}'
    response = client.get(url)
    assert response.status_code == 302  # Deve haver um redirecionamento
    assert response.url == reverse('edit_timetable') + f'?classs={class_instance.registration_class_id}'


# Teste para criação de grade horária com cursos válidos
@pytest.mark.django_db
def test_create_timetable_post_valid_courses(user, class_instance, course_instance, timeslot_instance):
    selected_courses = [
        {'course-123': timeslot_instance.hour_start + '-' + timeslot_instance.hour_end},
    ]
    data = {
        'selected_class': class_instance.registration_class_id,
        'selected_courses': json.dumps(selected_courses),
    }
    request = RequestFactory().post(reverse('create_timetable'), data=data)
    request.user = user
    response = create_timetable(request)
    assert response.status_code == 200  # Deve criar a grade horária com sucesso
    response_data = json.loads(response.content)
    assert response_data == {'erro': False, 'mensagem': ''}  # Deve ter a resposta esperada


# Teste para criação de grade horária com cursos válidos usando mocker
@pytest.mark.django_db
def test_create_timetable_post_valid_courses(user, class_instance, course_instance, timeslot_instance, mocker):
    data = {
        'selected_class': class_instance.registration_class_id,
        'selected_courses': json.dumps([['course-123']]),
    }
    request = RequestFactory().post(reverse('create_timetable'), data=data)
    request.user = user
    response = create_timetable(request)
    assert response.status_code == 200  # Deve criar a grade horária com sucesso
    response_data = json.loads(response.content)
    assert response_data == {'erro': False, 'mensagem': ''}  # Deve ter a resposta esperada


# Teste para criação de grade horária com classe inválida
@pytest.mark.django_db
def test_create_timetable_post_invalid_class(user, mocker):
    data = {
        'selected_class': 'invalid-class-id',  # Classe inválida
        'selected_courses': json.dumps([['course-123']]),
    }

    request = RequestFactory().post(reverse('create_timetable'), data=data)
    request.user = user
    response = create_timetable(request)

    assert response.status_code == 200  # Deve retornar com sucesso (mesmo que seja um erro)
    response_data = json.loads(response.content)
    assert response_data == {'erro': True, 'mensagem': 'Selecione uma turma válida'}


# Teste para criação de grade horária com curso inválido
@pytest.mark.django_db
def test_create_timetable_post_invalid_course(user, class_instance, mocker):
    # Dados fictícios
    data = {
        'selected_class': class_instance.registration_class_id,
        'selected_courses': json.dumps([['invalid-course-id']]),  # Curso inválido
    }

    # Simulando requisição post
    request = RequestFactory().post(reverse('create_timetable'), data=data)
    request.user = user
    response = create_timetable(request)

    assert response.status_code == 200  # Deve retornar com sucesso (mesmo que seja um erro)
    response_data = json.loads(response.content)
    assert response_data == {'erro': True, 'mensagem': 'Selecione uma disciplina válida'}


@pytest.fixture
def timetable_instance(django_db_setup, class_instance, course_instance, day_combo_instance, timeslot_instance):
    timetable = Timetable.objects.create(classs=class_instance, course=course_instance)
    day_combo = Day_combo.objects.create(day_combo_id=2, day='monday')
    # day_combo.timeslots.add(timeslot_instance)
    day_combo_instance.timeslots.add(timeslot_instance)
    timetable.day_combo.add(day_combo)
    return timetable


# Testes para editar grade horária
@pytest.mark.django_db
def test_edit_timetable_get_render(user, class_instance, course_instance, timetable_instance):
    # Teste para renderizar a página de edição da grade horária
    request = RequestFactory().get(reverse('edit_timetable') + f'?class={class_instance.registration_class_id}')
    request.user = user
    response = edit_timetable(request)

    assert response.status_code == 200  # Deve retornar com sucesso
    assert 'courses' in response.content.decode('utf-8')  # Deve conter os cursos no conteúdo
    assert 'timetable' in response.content.decode('utf-8')  # Deve conter a grade horária no conteúdo


# Testes para criar grade horária com classe inválida
@pytest.mark.django_db
def test_create_timetable_invalid_class(client, user, course_instance):
    # Teste para criar grade horária com classe inválida
    data = {
        'selected_class': 'invalid-class-id',
        'selected_courses': json.dumps([['course-123']]),
    }

    request = RequestFactory().post(reverse('create_timetable'), data=data)
    request.user = user
    response = create_timetable(request)

    assert response.status_code == 200  # Deve retornar com sucesso (mesmo que seja um erro)
    response_data = json.loads(response.content)
    assert response_data['erro'] is True
    assert response_data['mensagem'] == 'Selecione uma turma válida'


# Testes para criar grade horária com dados válidos
@pytest.mark.django_db
def test_create_timetable_valid_data(client, user, class_instance, course_instance, timeslot_instance):
    # Teste para criar grade horária com dados válidos
    data = {
        'selected_class': class_instance.registration_class_id,
        'selected_courses': json.dumps([['course-123']]),
    }

    request = RequestFactory().post(reverse('create_timetable'), data=data)
    request.user = user
    response = create_timetable(request)

    assert response.status_code == 200  # Deve retornar com sucesso
    response_data = json.loads(response.content)
    assert response_data == {'erro': False, 'mensagem': ""}


# Testes para editar grade horária
@pytest.mark.django_db
def test_edit_timetable_post_valid_data(client, user, class_instance, course_instance, timeslot_instance):
    # Teste para editar grade horária com dados válidos
    url = reverse('edit_timetable')
    selected_class = class_instance
    selected_class.registration_class_id = 'class-123'
    selected_class.save()

    client.force_login(user)

    data = {
        'selected_class': selected_class.registration_class_id,
        'selected_courses': json.dumps([['course-123']]),
    }

    request = RequestFactory().post(reverse('create_timetable'), data=data)
    request.user = user
    response = edit_timetable(request)

    assert response.status_code == 200  # Deve retornar com sucesso
    response_data = json.loads(response.content)
    assert response_data == {'erro': False, 'mensagem': ""}


# Testes para editar grade horária com classe inválida
@pytest.mark.django_db
def test_edit_timetable_post_invalid_class(client, user):
    # Teste para editar grade horária com classe inválida
    url = reverse('edit_timetable')

    client.force_login(user)

    data = {
        'selected_class': 'invalid-class-id',
        'selected_courses': json.dumps([['course-123']]),
    }

    request = RequestFactory().post(reverse('create_timetable'), data=data)
    request.user = user
    response = edit_timetable(request)

    assert response.status_code == 200  # Deve retornar com sucesso (mesmo que seja um erro)
    response_data = json.loads(response.content)
    assert response_data == {'erro': True, 'mensagem': 'Selecione uma turma válida'}


# Testes para editar grade horária com curso inválido
@pytest.mark.django_db
def test_edit_timetable_post_invalid_course(client, user, class_instance):
    # Teste para editar grade horária com curso inválido
    url = reverse('edit_timetable')

    client.force_login(user)

    data = {
        'selected_class': class_instance.registration_class_id,
        'selected_courses': json.dumps([['invalid-course-id']]),
    }

    request = RequestFactory().post(reverse('create_timetable'), data=data)
    request.user = user
    response = edit_timetable(request)

    assert response.status_code == 200  # Deve retornar com sucesso (mesmo que seja um erro)
    response_data = json.loads(response.content)
    assert response_data == {'erro': True, 'mensagem': 'Selecione uma disciplina válida'}


# Testes para timetable_combo_saver
@pytest.mark.django_db
def test_save_combo_day_existing_day_combo(course_instance, class_instance, timeslot_instance):
    # Teste para salvar combo de dia existente
    with transaction.atomic():  # Evita que os outros testes influenciem neste

        day_combo = Day_combo.objects.create(day='MONDAY')
        day_combo.timeslots.add(timeslot_instance)

        save_combo_day('MONDAY', [timeslot_instance], course_instance, class_instance)

    assert Timetable.objects.filter(course=course_instance, classs=class_instance).exists()


@pytest.mark.django_db
def test_save_combo_day_new_day_combo(course_instance, class_instance, timeslot_instance):
    # Teste para salvar novo combo de dia
    with transaction.atomic():
        save_combo_day('MONDAY', [timeslot_instance], course_instance, class_instance)

    assert Timetable.objects.filter(course=course_instance, classs=class_instance).exists()


class TimeslotFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Timeslot

    position = factory.Sequence(lambda n: n)
    hour_start = '08:00:00'
    hour_end = '10:00:00'


# Teste para timetable_combo_saver com vários cursos
@pytest.mark.django_db
def test_timetable_combo_saver_multiple_courses(course_instance, class_instance):
    timeslot_instance_1 = TimeslotFactory()
    timeslot_instance_2 = TimeslotFactory()

    # Cria cursos
    course_instance_1 = Course.objects.create(registration_course_id='course-321', area=class_instance.area)
    course_instance_2 = Course.objects.create(registration_course_id='course-654', area=class_instance.area)

    timetable = [
        [course_instance_1.registration_course_id, None],
        [course_instance_2.registration_course_id, course_instance_1.registration_course_id],
    ]

    timetable_combo_saver(timetable, class_instance)

    day_combos = Day_combo.objects.all()
    timetables = Timetable.objects.filter(classs=class_instance)

    # Verificações de como os combos foram salvos
    assert day_combos.count() == 3  # Deve haver 3 objetos Day_combo criados
    assert timetables.count() == 2  # Deve haver 2 objetos Timetable criados


# Teste para timetable_combo_saver com grade horária vazia
@pytest.mark.django_db
def test_timetable_combo_saver_empty_timetable(class_instance):
    timetable = [
        ['', '', ''],
        ['', '', ''],
    ]

    timetable_combo_saver(timetable, class_instance)

    day_combos = Day_combo.objects.all()
    timetables = Timetable.objects.filter(classs=class_instance)

    assert day_combos.count() == 0  # Nenhum objeto Day_combo deve ter sido criado
    assert timetables.count() == 0  # Nenhum objeto Timetable deve ter sido criado


# Teste para obter campo selecionado - critério válido
@pytest.mark.django_db
def test_get_selected_field_valid_criteria():
    criteria_career = Criteria.objects.create(is_select=False, number_criteria=2, name_criteria="date_career")
    criteria_birth = Criteria.objects.create(is_select=True, number_criteria=1, name_criteria="birth")

    result = get_selected_field()

    assert result == "birth"  # O campo selecionado deve ser "birth" (is_select=True)


# Teste para obter campo selecionado - critério inválido
@pytest.mark.django_db
def test_get_selected_field_invalid_criteria():
    criteria = Criteria.objects.create(is_select=True, number_criteria=10, name_criteria="Nome Inválido")

    result = get_selected_field()

    assert result == ""  # O campo selecionado deve ser vazio


User = get_user_model()


# Teste para criar fila de professores (sucesso)
@pytest.mark.django_db
def test_queue_create_success():
    factory = RequestFactory()

    # Cria um usuário
    user = User.objects.create_user(first_name='Magali', email='Magali@email.com', password='testpassword')

    # Cria uma requisição POST com os dados necessários
    request = factory.post('/detalhes-bloco/criar-fila', {
        'blockk_id': 'blockk_id',
        'table_data': json.dumps([
            [0, 'monica'],
            [1, 'cascão'],
            [2, 'chico']
        ]),
    })
    request.user = user

    # Criação de Blockk
    blockk = Blockk.objects.create(registration_block_id='blockk_id')

    # Criação de usuários
    User.objects.create(registration_id='chico', first_name='Chico', email='chico@email.com', cell_phone='1234567890')
    User.objects.create(registration_id='monica', first_name='Monica', email='monicao@email.com',
                        cell_phone='7234567899')
    User.objects.create(registration_id='cascão', first_name='Cascão', email='cascao@email.com',
                        cell_phone='9876543210')

    # Fazendo requisição à view
    response = queue_create(request)

    assert response.status_code == 200

    assert TeacherQueuePositionBackup.objects.filter(teacher__registration_id='monica', blockk=blockk).exists()
    assert TeacherQueuePositionBackup.objects.filter(teacher__registration_id='cascão', blockk=blockk).exists()
    assert TeacherQueuePositionBackup.objects.filter(teacher__registration_id='chico', blockk=blockk).exists()

    assert TeacherQueuePosition.objects.filter(teacher__registration_id='monica', blockk=blockk).exists()
    assert TeacherQueuePosition.objects.filter(teacher__registration_id='cascão', blockk=blockk).exists()
    assert TeacherQueuePosition.objects.filter(teacher__registration_id='chico', blockk=blockk).exists()

    monica_position_backup = TeacherQueuePositionBackup.objects.get(teacher__registration_id='monica',
                                                                    blockk=blockk).position
    chico_position_backup = TeacherQueuePositionBackup.objects.get(teacher__registration_id='chico',
                                                                   blockk=blockk).position
    cascao_position_backup = TeacherQueuePositionBackup.objects.get(teacher__registration_id='cascão',
                                                                    blockk=blockk).position

    monica_position = TeacherQueuePosition.objects.get(teacher__registration_id='monica', blockk=blockk).position
    chico_position = TeacherQueuePosition.objects.get(teacher__registration_id='chico', blockk=blockk).position
    cascao_position = TeacherQueuePosition.objects.get(teacher__registration_id='cascão', blockk=blockk).position

    assert monica_position_backup == 0
    assert cascao_position_backup == 1
    assert chico_position_backup == 2

    assert monica_position == 0
    assert cascao_position == 1
    assert chico_position == 2


# Teste para criar fila de professores com falha (bloco não encontrado)
@pytest.mark.django_db
def test_queue_create_failure_blockk_not_found():
    factory = RequestFactory()

    # Cria um usuário staff
    staff_user = User.objects.create_user(first_name='Magali', email='Magali@email.com', password='testpassword')

    # Cria uma requisição POST com um ID de bloco não existente
    request = factory.post('/detalhes-bloco/criar-fila/', {
        'blockk_id': 'non_existing_id',
        'table_data': json.dumps([
            [1, 'prof1_registration_id'],
        ]),
    })
    request.user = staff_user

    # Verifica se a exceção Blockk.DoesNotExist é lançada
    with pytest.raises(Blockk.DoesNotExist):
        response = queue_create(request)
