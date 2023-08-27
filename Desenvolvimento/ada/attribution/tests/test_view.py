import pytest
from datetime import datetime, timedelta
from django.test import RequestFactory
from area.models import Area, Blockk
from staff.models import Criteria, Deadline
from attribution.models import TeacherQueuePosition
from attribution.views import attribution, send_email, email_test, validations, manual_attribution_save, validate_timetable, assign_timetable_professor, professor_to_end_queue

from user.models import User
from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.mail import send_mail, EmailMessage
from django.core.mail import EmailMessage
import os
from unittest.mock import patch
from unittest.mock import Mock, patch, MagicMock
from timetable.models import Timetable, Timetable_user

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
