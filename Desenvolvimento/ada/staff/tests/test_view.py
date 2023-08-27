import pytest
import json
from datetime import datetime, timedelta
from user.models import User, History, AcademicDegree
from django.contrib.auth import get_user_model
from django.urls import reverse
from area.models import Blockk, Area
from enum import Enum
from staff.models import Deadline, Criteria
from staff.views import attribution_configuration_confirm, create_timetable, edit_timetable, save_combo_day, timetable_combo_saver, get_selected_field, calculate_total_score
import time
from unittest.mock import patch
from django.test import RequestFactory
from django.utils import timezone
from classs.models import Classs
from course.models import Course
# from faker import Faker
from timetable.models import Timetable, Day_combo, Timeslot
from django.urls import resolve
from django.db import transaction
import factory # cria vários registros fictícios automaticamente
from django.db.models import Sum
from datetime import date
from pytest_django.asserts import assertRedirects
from attribution.models import TeacherQueuePosition, TeacherQueuePositionBackup




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

@pytest.mark.django_db
def test_attribution_configuration_confirm(client_logged_in, blockk, deadlines):
    url = reverse('attribution_configuration_confirm')
    response = client_logged_in.post(url, {
        'blockk': blockk.registration_block_id,
        'startFPADeadline': deadlines.deadline_start.strftime("%Y-%m-%dT%H:%M"),
        'endFPADeadline': deadlines.deadline_end.strftime("%Y-%m-%dT%H:%M"),
        'startAssignmentDeadline': deadlines.deadline_start.strftime("%Y-%m-%dT%H:%M"),
        'endAssignmentDeadline': deadlines.deadline_end.strftime("%Y-%m-%dT%H:%M")
    })

    assert response.status_code == 200  # Verifica se a resposta é bem-sucedida

@pytest.fixture
def user(client):
    User = get_user_model()
    user = User.objects.create_user(registration_id='123', password='password', email="renato@email.com", is_staff=True)
    client.login(registration_id='123', password='password')
    return user

@pytest.mark.django_db
def test_update_save_with_existing_history(user, client):

    history = History.objects.create(
        birth='1990-01-01',
        date_career='2020-01-01',
        date_campus='2021-01-01',
        date_professor='2022-01-01',
        date_area='2023-01-01',
        date_institute='2024-01-01'
    )
    user.history = history
    user.save()

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

    response = client.post(reverse('update_save'), data=data)
    assert response.status_code == 200
    assert history.academic_degrees.count() == 1

@pytest.mark.django_db
def test_update_save_without_existing_history(user, client):
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

    response = client.post(reverse('update_save'), data=data)
    assert response.status_code == 200
    user.refresh_from_db()  # Refresh the user instance to get the updated history
    assert user.history is not None


@pytest.mark.django_db
def test_update_save_cleanup(user, client):

    academic_degree = AcademicDegree.objects.create(name='MSc', punctuation=3.5)

    data = {
        'registration_id': '123',
        'birth': '1990-01-01',
        'date_career': '2020-01-01',
        'date_campus': '2021-01-01',
        'date_professor': '2022-01-01',
        'date_area': '2023-01-01',
        'date_institute': '2024-01-01',
        'academic_degrees': '[]',
    }

    response = client.post(reverse('update_save'), data=data)
    assert response.status_code == 200
    assert not AcademicDegree.objects.filter(pk=academic_degree.pk).exists()

@pytest.mark.django_db
def test_update_save_no_access(client):
    # Create a non-staff user
    User = get_user_model()
    user = User.objects.create_user(registration_id='456', email="marcos@email.com", password='password', is_staff=False)
    client.login(registration_id='456', password='password')

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

    response = client.post(reverse('update_save'), data=data)
    assert response.status_code == 302  # Should be a redirection to the login page


@pytest.fixture
def area():
    return Area.objects.create(
        registration_area_id='area-1',
        name_area='Area 1',
        acronym='A1',
        exchange_area=True,
        is_high_school=True
    )

@pytest.mark.django_db
def test_classes_list(user, client):
    response = client.get(reverse('classes_list'))
    assert response.status_code == 200

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

# # Provável erro na view - TODO
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
@pytest.mark.django_db
def test_create_timetable_get_new_timetable_render(user, class_instance, client):
    response = client.get(reverse('create_timetable'), {'class': class_instance.registration_class_id})
    assert response.status_code == 200
    # assert 'selected_courses' in response.context
    assert 'timeslots' in response.context
    assert 'classs' in response.context
    assert 'courses' in response.context
#
#
@pytest.mark.django_db
def test_create_timetable_get_existing_timetable_redirect(user, class_instance, client):

    timetable = Timetable.objects.create(classs=class_instance)


    url = reverse('create_timetable') + f'?class={class_instance.registration_class_id}'
    response = client.get(url)

    assert response.status_code == 302
    assert response.url == reverse('edit_timetable') + f'?classs={class_instance.registration_class_id}'


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

    assert response.status_code == 200
    response_data = json.loads(response.content)
    assert response_data == {'erro': False, 'mensagem': ''}


@pytest.mark.django_db
def test_create_timetable_post_valid_courses(user, class_instance, course_instance, timeslot_instance, mocker):

    data = {
        'selected_class': class_instance.registration_class_id,
        'selected_courses': json.dumps([['course-123']]),
    }

    request = RequestFactory().post(reverse('create_timetable'), data=data)
    request.user = user
    response = create_timetable(request)

    assert response.status_code == 200
    response_data = json.loads(response.content)
    assert response_data == {'erro': False, 'mensagem': ''}

@pytest.mark.django_db
def test_create_timetable_post_invalid_class(user, mocker):

    data = {
        'selected_class': 'invalid-class-id',  # Classe inválida
        'selected_courses': json.dumps([['course-123']]),
    }

    request = RequestFactory().post(reverse('create_timetable'), data=data)
    request.user = user
    response = create_timetable(request)

    assert response.status_code == 200
    response_data = json.loads(response.content)
    assert response_data == {'erro': True, 'mensagem': 'Selecione uma turma válida'}

@pytest.mark.django_db
def test_create_timetable_post_invalid_course(user, class_instance, mocker):
    # dados fictícios
    data = {
        'selected_class': class_instance.registration_class_id,
        'selected_courses': json.dumps([['invalid-course-id']]),  # Curso inválido
    }

    # Simulando requisição post
    request = RequestFactory().post(reverse('create_timetable'), data=data)
    request.user = user
    response = create_timetable(request)

    assert response.status_code == 200
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
@pytest.mark.django_db
def test_edit_timetable_get_render(user, class_instance, course_instance, timetable_instance):
    request = RequestFactory().get(reverse('edit_timetable') + f'?class={class_instance.registration_class_id}')
    request.user = user
    response = edit_timetable(request)

    assert response.status_code == 200
    assert 'courses' in response.content.decode('utf-8')
    assert 'timetable' in response.content.decode('utf-8')

@pytest.mark.django_db
def test_create_timetable_invalid_class(client, user, course_instance):
    data = {
        'selected_class': 'invalid-class-id',
        'selected_courses': json.dumps([['course-123']]),
    }

    request = RequestFactory().post(reverse('create_timetable'), data=data)
    request.user = user
    response = create_timetable(request)

    assert response.status_code == 200
    response_data = json.loads(response.content)
    assert response_data['erro'] is True
    assert response_data['mensagem'] == 'Selecione uma turma válida'


@pytest.mark.django_db
def test_create_timetable_valid_data(client, user, class_instance, course_instance, timeslot_instance):
    data = {
        'selected_class': class_instance.registration_class_id,
        'selected_courses': json.dumps([['course-123']]),
    }

    request = RequestFactory().post(reverse('create_timetable'), data=data)
    request.user = user
    response = create_timetable(request)

    assert response.status_code == 200
    response_data = json.loads(response.content)
    assert response_data == {'erro': False, 'mensagem': ""}

# Testes edit timetable
@pytest.mark.django_db
def test_edit_timetable_post_valid_data(client, user, class_instance, course_instance, timeslot_instance):
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

    assert response.status_code == 200
    response_data = json.loads(response.content)
    assert response_data == {'erro': False, 'mensagem': ""}


@pytest.mark.django_db
def test_edit_timetable_post_invalid_class(client, user):
    url = reverse('edit_timetable')

    client.force_login(user)

    data = {
        'selected_class': 'invalid-class-id',
        'selected_courses': json.dumps([['course-123']]),
    }

    request = RequestFactory().post(reverse('create_timetable'), data=data)
    request.user = user
    response = edit_timetable(request)

    assert response.status_code == 200
    response_data = json.loads(response.content)
    assert response_data == {'erro': True, 'mensagem': 'Selecione uma turma válida'}


@pytest.mark.django_db
def test_edit_timetable_post_invalid_course(client, user, class_instance):
    url = reverse('edit_timetable')

    client.force_login(user)

    data = {
        'selected_class': class_instance.registration_class_id,
        'selected_courses': json.dumps([['invalid-course-id']]),
    }

    request = RequestFactory().post(reverse('create_timetable'), data=data)
    request.user = user
    response = edit_timetable(request)

    assert response.status_code == 200
    response_data = json.loads(response.content)
    assert response_data == {'erro': True, 'mensagem': 'Selecione uma disciplina válida'}


# Testes timetable_combo_saver timetable
@pytest.mark.django_db
def test_save_combo_day_existing_day_combo(course_instance, class_instance, timeslot_instance):
    with transaction.atomic(): # evita que os outros testes influencie nesse

        day_combo = Day_combo.objects.create(day='MONDAY')
        day_combo.timeslots.add(timeslot_instance)

        save_combo_day('MONDAY', [timeslot_instance], course_instance, class_instance)

    assert Timetable.objects.filter(course=course_instance, classs=class_instance).exists()

@pytest.mark.django_db
def test_save_combo_day_new_day_combo(course_instance, class_instance, timeslot_instance):
    with transaction.atomic():

        save_combo_day('MONDAY', [timeslot_instance], course_instance, class_instance)

    assert Timetable.objects.filter(course=course_instance, classs=class_instance).exists()

# Testes timetable_combo_saver - unitário
class TimeslotFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Timeslot

    position = factory.Sequence(lambda n: n)
    hour_start = '08:00:00'
    hour_end = '10:00:00'

@pytest.mark.django_db
def test_timetable_combo_saver_multiple_courses(course_instance, class_instance):
    timeslot_instance_1 = TimeslotFactory()
    timeslot_instance_2 = TimeslotFactory()

    # Criar cursos
    course_instance_1 = Course.objects.create(registration_course_id='course-321', area=class_instance.area)
    course_instance_2 = Course.objects.create(registration_course_id='course-654', area=class_instance.area)

    timetable = [
        [course_instance_1.registration_course_id, None],
        [course_instance_2.registration_course_id, course_instance_1.registration_course_id],
    ]

    timetable_combo_saver(timetable, class_instance)

    day_combos = Day_combo.objects.all()
    timetables = Timetable.objects.filter(classs=class_instance)

    # salvado course-321 no dia monday, nos horários [0]
    # [0]
    # salvado course-654 no dia tuesday, nos horários [0]
    # [1]
    # salvado course-654 no dia tuesday, nos horários [1]
    # ?????????

    assert day_combos.count() == 3
    assert timetables.count() == 2

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

# Teste get_selected field - unitário
@pytest.mark.django_db
def test_get_selected_field_valid_criteria():
    criteria = Criteria.objects.create(is_select=True, number_criteria=1, name_criteria="Nome do Critério")

    result = get_selected_field()
    assert result == "birth"

@pytest.mark.django_db
def test_get_selected_field_invalid_criteria():
    criteria = Criteria.objects.create(is_select=True, number_criteria=10, name_criteria="Nome Inválido")

    result = get_selected_field()
    assert result == ""


# Testes queue_create

