import pytest
import json
from datetime import datetime, timedelta
from user.models import User, History, AcademicDegree
from django.contrib.auth import get_user_model
from django.urls import reverse
from area.models import Blockk, Area
from enums import enum
from staff.models import Deadline
from staff.views import attribution_configuration_confirm, show_current_deadline
import time
from unittest.mock import patch
from django.test import RequestFactory
from django.utils import timezone
from classs.models import Classs
from course.models import Course
#from faker import Faker
from timetable.models import Timetable, Day_combo


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

# @pytest.mark.django_db
# def test_show_current_deadline():
#     # Crie instâncias de Deadline para os testes
#     start_fpa = Deadline.objects.create(name="startFPADeadline", deadline_start=timezone.now(), deadline_end=timezone.now() + timezone.timedelta(hours=1))
#     start_assignment = Deadline.objects.create(name="startAssignmentDeadline", deadline_start=timezone.now() - timezone.timedelta(hours=1), deadline_end=timezone.now() + timezone.timedelta(hours=1))
#     start_exchange = Deadline.objects.create(name="startExchangeDeadline", deadline_start=timezone.now() - timezone.timedelta(hours=2), deadline_end=timezone.now() - timezone.timedelta(hours=1))
#
#     factory = RequestFactory()
#     request = factory.get(reverse('show_current_deadline'))
#
#     response = show_current_deadline(request)
#
#     assert response.status_code == 200
#
#     # Verifique se o contexto da resposta contém a chave 'actualDeadline'
#     assert 'actualDeadline' in response.context
#
#     # Verifique se a resposta renderiza o template correto
#     assert 'staff/deadline/show_current_deadline.html' in response.template_name
#
#     # Verifique se o contexto contém o valor correto para 'actualDeadline'
#     assert response.context['actualDeadline'] == "FPA"


@pytest.fixture
def user(client):
    User = get_user_model()
    user = User.objects.create_user(registration_id='123', password='password', email="renato@email.com", is_staff=True)
    client.login(registration_id='123', password='password')
    return user

@pytest.mark.django_db
def test_update_save_with_existing_history(user, client):
    # Create an existing history for the user
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

# Test cleanup of unused academic degrees
@pytest.mark.django_db
def test_update_save_cleanup(user, client):
    # Create an unused academic degree
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

# Test user without staff access
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
        name_block='Test Block'
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


@pytest.fixture
def timetable_instance(django_db_setup, class_instance):
    return Timetable.objects.create(
        classs=class_instance,
        day='Monday',
        start_time='08:00',
        end_time='10:00'
    )


@pytest.fixture
def timetable_instance(django_db_setup, class_instance):
    return Timetable.objects.create(classs=class_instance)

@pytest.fixture
def timeslot_instance(django_db_setup):
    return Timeslot.objects.create(hour_start='08:00', hour_end='10:00')

@pytest.fixture
def day_combo_instance(django_db_setup, timeslot_instance):
    return Day_combo.objects.create(day=Day.MONDAY.name)

@pytest.fixture
def timetable_user_instance(django_db_setup, timetable_instance, user):
    return Timetable_user.objects.create(timetable=timetable_instance, user=user)


@pytest.mark.django_db
def test_timetables_view(user, block_instance, area_instance, class_instance, timetable_instance, client):
    client.force_login(user)
    url = reverse('timetables')

    response = client.get(url)
    assert response.status_code == 200

    assert 'timetables' in response.context
    assert 'user_blocks' in response.context
    assert 'classes' in response.context
