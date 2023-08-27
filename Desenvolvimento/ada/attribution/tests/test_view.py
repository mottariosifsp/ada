import pytest
from datetime import datetime, timedelta
from django.test import RequestFactory
from area.models import Area, Blockk
from staff.models import Criteria, Deadline
from attribution.models import TeacherQueuePosition
from attribution.views import attribution, send_email, attribution_detail, email_test, validations, manual_attribution_save, validate_timetable, assign_timetable_professor, professor_to_end_queue, attribution_detail, remove_professors_without_preference, float_to_time, start_attribution
from classs.models import Classs
from area.models import Area, Blockk
from user.models import User
from django.test import Client
from course.models import Course
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.mail import send_mail, EmailMessage
from django.core.mail import EmailMessage
import os
from datetime import timedelta
from unittest.mock import patch
from unittest.mock import Mock, patch, MagicMock
from timetable.models import Timetable, Timeslot, Timetable_user, Day_combo
from datetime import time
from attribution_preference.models import Course_preference, Attribution_preference
from django.utils import timezone

User = get_user_model()

@pytest.fixture
def superuser():
    return User.objects.create_user(
        first_name='Super',
        last_name='User',
        email='superuser@example.com',
        password='testpassword',
        is_superuser=True
    )

@pytest.mark.django_db
@patch('attribution.views.send_email')
def test_email_test_view(mock_send_email, superuser, rf):
    request = rf.post('/email_test/')
    request.user = superuser

    response = email_test(request)

    assert response.status_code == 302
    assert response.url == '/atribuicao/email_test/'

    assert mock_send_email.called
    assert mock_send_email.call_count == 1
    assert mock_send_email.call_args[0][0] == superuser


class MockEmailMessage:
    def __init__(self, *args, **kwargs):
        pass

    def send(self):
        pass

class MockProfessor:
    def __init__(self, first_name, email):
        self.first_name = first_name
        self.email = email

def test_send_email():
    professor = MockProfessor('John', 'john@example.com')

    with patch('django.core.mail.EmailMessage', MockEmailMessage):
        send_email(professor)


@pytest.fixture
def timetable():
    return Mock(spec=Timetable)

@pytest.fixture
def professor():
    return Mock()

@patch('timetable.models.Timetable_user.objects')
def test_validations_with_no_existing_timetable_user(mock_objects, timetable, professor):
    mock_objects.filter.return_value.exists.return_value = False
    mock_objects.create.return_value = Timetable_user(user=None)

    result = validations(timetable, professor)

    assert result == True

@patch('timetable.models.Timetable_user.objects')
def test_validations_with_existing_timetable_user_and_no_assigned_user(mock_objects, timetable, professor):
    mock_objects.filter.return_value.exists.return_value = True
    mock_objects.get.return_value = Timetable_user(user=None)

    result = validations(timetable, professor)

    assert result == True

@patch('timetable.models.Timetable_user.objects')
def test_validations_with_existing_timetable_user_and_assigned_user(mock_objects, timetable, professor):
    timetable_user_mock = Mock(spec=Timetable_user)
    timetable_user_mock.user = professor
    mock_objects.filter.return_value.exists.return_value = True
    mock_objects.get.return_value = timetable_user_mock

    result = validations(timetable, professor)

    assert result == False

@pytest.fixture
def timetables():
    return [Mock(), Mock(), Mock()]

@pytest.fixture
def professor():
    return Mock()

@pytest.fixture
def blockk():
    return Mock()


@patch('attribution.views.TeacherQueuePosition.objects')
@patch('attribution.views.validate_timetable')
@patch('attribution.views.assign_timetable_professor')
@patch('attribution.views.professor_to_end_queue')
def test_manual_attribution_save_successful(mock_professor_to_end_queue, mock_assign_timetable_professor, mock_validate_timetable, mock_teacher_queue_position_objects, timetables, professor, blockk):
    mock_teacher_queue_position_objects.get.return_value.teacher.first_name = professor.first_name
    mock_teacher_queue_position_objects.get.return_value.teacher = professor

    mock_validate_timetable.return_value = True

    result = manual_attribution_save(timetables, professor, blockk)

    assert result is None
    assert mock_teacher_queue_position_objects.filter.called
    assert mock_assign_timetable_professor.call_count == len(timetables)
    assert mock_professor_to_end_queue.called

@patch('attribution.views.TeacherQueuePosition.objects')
def test_manual_attribution_save_invalid_teacher(mock_teacher_queue_position_objects, timetables, professor, blockk):
    mock_teacher_queue_position_objects.get.return_value.teacher.first_name = 'Another Professor'
    mock_teacher_queue_position_objects.get.return_value.teacher == professor

    result = manual_attribution_save(timetables, professor, blockk)

    assert result == False

# @patch('attribution.views.TeacherQueuePosition.objects')
# @patch('attribution.views.validate_timetable')
# def test_manual_attribution_save_with_invalid_timetables(mock_validate_timetable, mock_teacher_queue_position_objects, timetables, professor, blockk):
#     mock_teacher_queue_position_objects.get.return_value.teacher = professor
#     mock_validate_timetable.side_effect = [False, True, False]
#
#     result = manual_attribution_save(timetables, professor, blockk)
#
#     assert isinstance(result, list)
#     assert len(result) == 2
#     assert mock_teacher_queue_position_objects.filter.called


@pytest.mark.django_db
def test_attribution_detail_sucess(rf):

    your_area_instance = Area.objects.create(
        registration_area_id='test_area',
        name_area='Test Area',
        acronym='TA',
        exchange_area=True,
        is_high_school=True
    )

    your_class_instance = Classs.objects.create(
        registration_class_id='test_class',
        period='Some Period',
        semester=1,
        area=your_area_instance
    )

    your_timetable_instance = Timetable.objects.create(classs=your_class_instance)

    your_timeslot_instance = Timeslot.objects.create(
        position=1,
        hour_start='08:00',
        hour_end='09:00'
    )

    your_day_combo_instance = Day_combo.objects.create(day='monday')

    your_course_instance = Course.objects.create(
        registration_course_id='test_course',
        name_course='Test Course',
        acronym='TC',
        area=your_area_instance,
        blockk=None
    )

    your_timetable_instance.course = your_course_instance
    your_timetable_instance.save()


    timetable_user = Timetable_user.objects.create(timetable=your_timetable_instance)
    timetable_user.timetable.day_combo.add(your_day_combo_instance)

    request = rf.get(reverse('attribution:attribution_detail'), {'class': your_class_instance.registration_class_id})

    response = attribution_detail(request)

    assert response.status_code == 200

@pytest.mark.django_db
def test_remove_professors_without_preference():

    your_blockk_instance = Blockk.objects.create(
        registration_block_id='test_blockk',
        name_block='Test Blockk',
        acronym='TB'
    )

    user_with_preference = User.objects.create_user(
        registration_id='123456789',
        first_name='UserWithPreference',
        email='userwithpreference@example.com',
        cell_phone='1234567890',
        is_professor=True
    )
    user_without_preference = User.objects.create_user(
        registration_id='987654321',
        first_name='UserWithoutPreference',
        email='userwithoutpreference@example.com',
        cell_phone='9876543210',
        is_professor=True
    )

    TeacherQueuePosition.objects.create(teacher=user_with_preference, position=1, blockk=your_blockk_instance)
    TeacherQueuePosition.objects.create(teacher=user_without_preference, position=2, blockk=your_blockk_instance)

    remove_professors_without_preference(your_blockk_instance)

    # usuário sem preferência foi removido da fila
    assert not TeacherQueuePosition.objects.filter(teacher=user_without_preference,
                                                   blockk=your_blockk_instance).exists()

    # assert TeacherQueuePosition.objects.filter(teacher=user_with_preference, blockk=your_blockk_instance).exists() ?


def test_float_to_time_positive():
    seconds = 3661  # 1 hora, 1 minuto e 1 segundo
    result = float_to_time(seconds)
    assert result.hour == 1
    assert result.minute == 1
    assert result.second == 1

def test_float_to_time_zero():
    seconds = 0
    result = float_to_time(seconds)
    assert result.hour == 0
    assert result.minute == 0
    assert result.second == 0

def test_float_to_time_negative():
    seconds = -3600  # -1 hora
    result = float_to_time(seconds)
    assert result.hour == 0
    assert result.minute == 0
    assert result.second == 0


# manual_attribution

# next_attribution

# start_attribution
# @pytest.mark.django_db
# def test_start_attribution_with_professors_in_queue():
#
#     your_area_instance = Area.objects.create(
#         registration_area_id='test_area',
#         name_area='Test Area',
#         acronym='TA',
#         exchange_area=True,
#         is_high_school=True
#     )
#
#     # Crie objetos de teste necessários
#     your_blockk_instance = Blockk.objects.create(
#         registration_block_id='test_block',
#         name_block='Test Block',
#         acronym='TB'
#     )
#
#     your_user_instance = User.objects.create(
#         registration_id='12345',
#         first_name='John',
#         last_name='Doe',
#         email='john@example.com',
#         cell_phone='1234567890'
#         # Preencha outros campos conforme necessário
#     )
#
#     your_class_instance2 = Classs.objects.create(
#         registration_class_id='test_class',
#         period='Some Period',
#         semester=1,
#         area=your_area_instance
#     )
#
#
#     TeacherQueuePosition.objects.create(
#         teacher=your_user_instance,
#         position=0,
#         blockk=your_blockk_instance
#     )
#
#     attribution_preference = Attribution_preference.objects.create(user=your_user_instance)
#     your_timetable_instance = Timetable.objects.create(classs=your_class_instance2)
#
#     Course_preference.objects.create(
#         attribution_preference=attribution_preference,
#         timetable=your_timetable_instance,
#         blockk=your_blockk_instance
#     )
#
#     start_attribution(your_blockk_instance)

@pytest.mark.django_db
def test_start_attribution_with_empty_queue():

    your_blockk_instance = Blockk.objects.create(
        registration_block_id='test_block',
        name_block='Test Block',
        acronym='TB'
    )

    Deadline.objects.create(
        blockk=your_blockk_instance,
        name='STARTASSIGNMENTDEADLINE',
        deadline_start=timezone.now(),
        deadline_end=timezone.now() + timezone.timedelta(hours=1) #uma hora após agora
    )

    start_attribution(your_blockk_instance)

    deadline = Deadline.objects.get(blockk=your_blockk_instance, name='STARTASSIGNMENTDEADLINE')
    assert deadline.deadline_end <= timezone.now()