import pytest
from datetime import datetime, timedelta
from django.test import RequestFactory
from area.models import Area, Blockk
from staff.models import Criteria, Deadline
from attribution.models import TeacherQueuePosition
from attribution.views import attribution, send_email, next_attribution, attribution_detail, email_test, validations, manual_attribution_save, validate_timetable, assign_timetable_professor, professor_to_end_queue, attribution_detail, remove_professors_without_preference, float_to_time, start_attribution, create_cord
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
@patch('attribution.views.send_email')  # Usando patch para substituir temporariamente a função send_email
def test_email_test_view(mock_send_email, superuser, rf):
    # Cria uma solicitação HTTP simulada usando o RequestFactory
    request = rf.post('/email_test/')
    request.user = superuser  # Define o usuário da solicitação como um superusuário simulado

    # Chama a função email_test da visualização, passando a solicitação simulada
    response = email_test(request)

    # Verificações de asserção para garantir que a visualização se comporta conforme o esperado
    assert response.status_code == 302  # Deve redirecionar após o envio de email
    assert response.url == '/atribuicao/email_test/'  # Deve redirecionar para a URL '/atribuicao/email_test/'

    assert mock_send_email.called  # Verifica se a função send_email foi chamada
    assert mock_send_email.call_count == 1  # Deve ter sido chamada apenas uma vez
    assert mock_send_email.call_args[0][0] == superuser  # Verifica se o argumento passado para send_email é o superusuário



class MockEmailMessage:
    def __init__(self, *args, **kwargs):
        pass

    def send(self):
        pass

class MockProfessor:
    def __init__(self, first_name, email):
        self.first_name = first_name
        self.email = email

@pytest.mark.django_db
def test_send_email():
    # Cria uma instância simulada de um professor com nome e email
    professor = MockProfessor('John', 'john@example.com')

    # Simula o comportamento de 'django.core.mail.EmailMessage' usando a classe MockEmailMessage
    # Isso é feito por meio do uso do patch
    with patch('django.core.mail.EmailMessage', MockEmailMessage):
        # Chama a função send_email com a instância simulada de professor
        send_email(professor)


@pytest.fixture
def timetable():
    return Mock(spec=Timetable)

@pytest.fixture
def professor():
    return Mock()

@patch('timetable.models.Timetable_user.objects')
@pytest.mark.django_db
def test_validations_with_no_existing_timetable_user(mock_objects, timetable, professor):
    # Simula que não existe Timetable_user para o professor
    mock_objects.filter.return_value.exists.return_value = False
    mock_objects.create.return_value = Timetable_user(user=None)

    # Chama a função de validação com um Timetable e um professor
    result = validations(timetable, professor)

    # Verifica se o resultado é True, indicando que as validações passaram
    assert result == True

@patch('timetable.models.Timetable_user.objects')
@pytest.mark.django_db
def test_validations_with_existing_timetable_user_and_no_assigned_user(mock_objects, timetable, professor):
    # Simula que já existe um Timetable_user para o professor, mas ainda não está atribuído
    mock_objects.filter.return_value.exists.return_value = True
    mock_objects.get.return_value = Timetable_user(user=None)

    # Chama a função de validação com um Timetable e um professor
    result = validations(timetable, professor)

    # Verifica se o resultado é True, indicando que as validações passaram
    assert result == True

@patch('timetable.models.Timetable_user.objects')
@pytest.mark.django_db
def test_validations_with_existing_timetable_user_and_assigned_user(mock_objects, timetable, professor):
    # Simula que já existe um Timetable_user para o professor e ele já está atribuído a um usuário
    timetable_user_mock = Mock(spec=Timetable_user)
    timetable_user_mock.user = professor
    mock_objects.filter.return_value.exists.return_value = True
    mock_objects.get.return_value = timetable_user_mock

    # Chama a função de validação com um Timetable e um professor
    result = validations(timetable, professor)

    # Verifica se o resultado é False, indicando que as validações não passaram
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
@pytest.mark.django_db
def test_manual_attribution_save_successful(
    mock_professor_to_end_queue,
    mock_assign_timetable_professor,
    mock_validate_timetable,
    mock_teacher_queue_position_objects,
    timetables,
    professor,
    blockk
):  # Configuração de mock para testar atribuição manual bem-sucedida

    # Configura o mock para retornar o nome do professor corretamente
    mock_teacher_queue_position_objects.get.return_value.teacher.first_name = professor.first_name
    # Configura o mock para retornar a instância do professor correta
    mock_teacher_queue_position_objects.get.return_value.teacher = professor

    # Configura o mock para validar a tabela de horários
    mock_validate_timetable.return_value = True

    # Chama a função de atribuição manual
    result = manual_attribution_save(timetables, professor, blockk)

    # Verifica os resultados esperados
    assert result is None  # O resultado deve ser None para uma atribuição bem-sucedida
    assert mock_teacher_queue_position_objects.filter.called  # Deve ter sido chamado filter do mock
    assert mock_assign_timetable_professor.call_count == len(timetables)  # Deve ter sido chamado assign_timetable_professor para cada horário
    assert mock_professor_to_end_queue.called  # Deve ter sido chamado professor_to_end_queue

@patch('attribution.views.TeacherQueuePosition.objects')
@pytest.mark.django_db
def test_manual_attribution_save_invalid_teacher(mock_teacher_queue_position_objects, timetables, professor, blockk):
    # Configuração de mock para testar atribuição manual com professor inválido

    # Configura o mock para retornar um nome de professor diferente
    mock_teacher_queue_position_objects.get.return_value.teacher.first_name = 'Another Professor'
    # Configura o mock para retornar a instância do professor correta
    mock_teacher_queue_position_objects.get.return_value.teacher == professor

    # Chame a função de atribuição manual
    result = manual_attribution_save(timetables, professor, blockk)

    assert result == False  # O resultado deve ser False para um professor inválido

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
    # Cria uma instância de Área
    area_instance = Area.objects.create(
        registration_area_id='test_area',
        name_area='Test Area',
        acronym='TA',
        exchange_area=True,
        is_high_school=True
    )

    # Cria uma instância de Classs
    class_instance = Classs.objects.create(
        registration_class_id='test_class',
        period='Some Period',
        semester=1,
        area=area_instance
    )

    # Cria uma instância de Timetable
    timetable_instance = Timetable.objects.create(classs=class_instance)

    # Cria uma instância de Timeslot
    timeslot_instance = Timeslot.objects.create(
        position=1,
        hour_start='08:00',
        hour_end='09:00'
    )

    # Cria uma instância de Day_combo
    day_combo_instance = Day_combo.objects.create(day='monday')

    # Cria uma instância de Course
    course_instance = Course.objects.create(
        registration_course_id='test_course',
        name_course='Test Course',
        acronym='TC',
        area=area_instance,
        blockk=None
    )

    # Associa o curso à instância de Timetable
    timetable_instance.course = course_instance
    timetable_instance.save()

    # Cria uma instância de Timetable_user e associa o Day_combo a ela
    timetable_user = Timetable_user.objects.create(timetable=timetable_instance)
    timetable_user.timetable.day_combo.add(day_combo_instance)

    # Cria uma requisição GET para a view attribution_detail
    request = rf.get(reverse('attribution:attribution_detail'), {'class': class_instance.registration_class_id})

    # Chama a view attribution_detail com a requisição criada
    response = attribution_detail(request)

    assert response.status_code == 200  # O código de resposta deve ser 200 (OK)

@pytest.mark.django_db
def test_remove_professors_without_preference():
    # Teste para verificar se os professores sem preferência são removidos da fila

    # Cria uma instância de Blockk
    blockk_instance = Blockk.objects.create(
        registration_block_id='test_blockk',
        name_block='Test Blockk',
        acronym='TB'
    )

    # Usuário com preferência
    user_with_preference = User.objects.create_user(
        registration_id='123456789',
        first_name='UserWithPreference',
        email='userwithpreference@example.com',
        cell_phone='1234567890',
        is_professor=True
    )

    # Usuário sem preferência
    user_without_preference = User.objects.create_user(
        registration_id='987654321',
        first_name='UserWithoutPreference',
        email='userwithoutpreference@example.com',
        cell_phone='9876543210',
        is_professor=True
    )

    # Cria instâncias de TeacherQueuePosition para ambos os usuários
    TeacherQueuePosition.objects.create(teacher=user_with_preference, position=1, blockk=blockk_instance)
    TeacherQueuePosition.objects.create(teacher=user_without_preference, position=2, blockk=blockk_instance)

    # Chama a função para remover professores sem preferência da fila
    remove_professors_without_preference(blockk_instance)

    # Verifica se o usuário sem preferência foi removido da fila
    assert not TeacherQueuePosition.objects.filter(teacher=user_without_preference,
                                                   blockk=blockk_instance).exists()

    # assert TeacherQueuePosition.objects.filter(teacher=user_with_preference, blockk=your_blockk_instance).exists() ?


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
#     TeacherQueuePosition.objects.create(
#         teacher=your_user_instance,
#         position=0,
#         blockk=your_blockk_instance
#     )
#
#     attribution_preference = Attribution_preference.objects.create(user=your_user_instance)
#
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

    blockk_instance = Blockk.objects.create(
        registration_block_id='test_block',
        name_block='Test Block',
        acronym='TB'
    )

    Deadline.objects.create(
        blockk=blockk_instance,
        name='STARTASSIGNMENTDEADLINE',
        deadline_start=timezone.now(),
        deadline_end=timezone.now() + timezone.timedelta(hours=1) # uma hora após agora
    )

    # Chama a função start_attribution() com a instância de Blockk criada
    start_attribution(blockk_instance)

    # Obtém a instância de Deadline criada
    deadline = Deadline.objects.get(blockk=blockk_instance, name='STARTASSIGNMENTDEADLINE')

    # Verifica se o prazo de término é anterior ou igual ao horário atual
    assert deadline.deadline_end <= timezone.now()

# manual_attribution

# next_attribution

@pytest.mark.django_db
def test_next_attribution_no_primary_timetables(mocker):
    # Mock para a função timetables_preference.filter()
    mock_timetables_preference = Mock()
    mock_timetables_preference.filter.return_value = mock_timetables_preference
    mock_timetables_preference.values_list.return_value = []

    # Mock para o objeto Professor na fila
    mock_next_professor_in_queue = Mock()
    mock_next_professor_in_queue.teacher.first_name = "John"

    # Mock para o objeto Blockk
    mock_blockk = Mock()

    # Mock para a função ids_to_timetables()
    mock_ids_to_timetables = mocker.patch("attribution.views.ids_to_timetables")
    mock_ids_to_timetables.return_value = []

    # Mock para a função create_cord()
    mock_create_cord = mocker.patch("attribution.views.create_cord")
    mock_create_cord.return_value = []

    # Mock para a função validate_timetable()
    mock_validate_timetable = mocker.patch("attribution.views.validate_timetable")
    mock_validate_timetable.return_value = True

    # Mock para a função assign_timetable_professor()
    mock_assign_timetable_professor = mocker.patch("attribution.views.assign_timetable_professor")

    # Mock para a função professor_to_end_queue()
    mock_professor_to_end_queue = mocker.patch("attribution.views.professor_to_end_queue")

    # Mock para a função cancel_scheduled_task()
    mock_cancel_scheduled_task = mocker.patch("attribution.views.cancel_scheduled_task")

    # Mock para a função start_attribution()
    mock_start_attribution = mocker.patch("attribution.views.start_attribution")

    # Chama a função next_attribution() com os mocks criados
    result = next_attribution(
        mock_timetables_preference,
        mock_next_professor_in_queue,
        mock_blockk
    )

    # Verifica se as funções mock foram chamadas
    assert mock_professor_to_end_queue.called
    assert mock_next_professor_in_queue.delete.called
    assert mock_cancel_scheduled_task.called
    assert mock_start_attribution.called

    # Verifica se o resultado é o esperado
    assert result == mock_start_attribution.return_value

#                   #
#  Testes unitário  #
#                   #
@pytest.mark.django_db
def test_create_cord():
    # instância de área
    area_instance = Area.objects.create(
        registration_area_id='test_area',
        name_area='Test Area',
        acronym='TA',
        exchange_area=True,
        is_high_school=True
    )

    # instância de turma associada à área
    class_instance = Classs.objects.create(
        registration_class_id='test_class',
        period='Some Period',
        semester=1,
        area=area_instance
    )

    # instância de horário associada à turma
    timetable = Timetable.objects.create(classs=class_instance)

    # instâncias de combos de dia
    day_combo_1 = Day_combo.objects.create(day='Segunda')
    day_combo_2 = Day_combo.objects.create(day='Terça')

    # instâncias de horários
    timeslot_1 = Timeslot.objects.create(position=1, hour_start=time(8, 0), hour_end=time(9, 0))
    timeslot_2 = Timeslot.objects.create(position=2, hour_start=time(9, 0), hour_end=time(10, 0))

    # Associação de horários aos combos de dia
    day_combo_1.timeslots.set([timeslot_1, timeslot_2])
    day_combo_2.timeslots.set([timeslot_1])

    # Associação combos de dia ao horário
    timetable.day_combo.set([day_combo_1, day_combo_2])

    cords = create_cord(timetable)

    # Cords esperados
    expected_cords = ['1-Segunda', '2-Segunda', '1-Terça']

    # Verifica se os cords gerados correspondem aos esperados
    assert cords == expected_cords

def test_float_to_time_positive():
    # Teste para converter segundos em formato de tempo positivo
    seconds = 3661  # 1 hora, 1 minuto e 1 segundo
    result = float_to_time(seconds)
    assert result.hour == 1  # Deve ser 1 hora
    assert result.minute == 1  # Deve ser 1 minuto
    assert result.second == 1  # Deve ser 1 segundo

def test_float_to_time_zero():
    # Teste para converter segundos em formato de tempo igual a zero
    seconds = 0
    result = float_to_time(seconds)
    assert result.hour == 0  # Deve ser 0 horas
    assert result.minute == 0  # Deve ser 0 minutos
    assert result.second == 0  # Deve ser 0 segundos

def test_float_to_time_negative():
    # Teste para converter segundos em formato de tempo negativo
    seconds = -3600  # -1 hora
    result = float_to_time(seconds)
    assert result.hour == 0  # Deve ser 0 horas (não deve ser negativo)
    assert result.minute == 0  # Deve ser 0 minutos (não deve ser negativo)
    assert result.second == 0  # Deve ser 0 segundos (não deve ser negativo)