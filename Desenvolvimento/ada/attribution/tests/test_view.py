import pytest
from datetime import datetime, timedelta
from django.test import RequestFactory
from area.models import Area, Blockk
from staff.models import Criteria, Deadline
from attribution.models import TeacherQueuePosition
from attribution.views import attribution, send_email, email_test
from user.models import User
from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.mail import send_mail, EmailMessage
from django.core.mail import EmailMessage
import os
from unittest.mock import patch

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

