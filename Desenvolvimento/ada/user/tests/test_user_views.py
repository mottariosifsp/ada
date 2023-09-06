import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import Client
from django.http import HttpRequest
from django.contrib.auth.forms import AuthenticationForm
from user.views import handler500, provocar_erro_500

@pytest.fixture # usado em todos os testes
def client():
    return Client()

@pytest.fixture
def user():
    return get_user_model().objects.create_user(
        first_name='Joao',
        email='joao@email.com',
        password='password'
    )

def test_login_view(client):
    response = client.get(reverse('login'))
    assert response.status_code == 200
    assert 'form' in response.context
    assert 'registration/login.html' in [template.name for template in response.templates]

@pytest.mark.django_db
def test_login_post(client):
    data = {'first_name': 'João', 'email': 'joao@email.com', 'password': 'password123'}
    response = client.post(reverse('login'), data=data)

    assert response.status_code == 200

    assert 'registration/login.html' in [template.name for template in response.templates]

    # verifica se tem um form na requisição
    assert isinstance(response.context['form'], AuthenticationForm)

@pytest.mark.django_db # permite acessar o banco de dados
def test_home_view_authenticated_staff(client, user):
    user.is_staff = True
    user.is_professor = False
    user.is_superuser = False
    user.save()

    client.force_login(user)

    response = client.get(reverse('home'))
    assert response.status_code == 302
    assert response.url == reverse('home_staff')

# Se o usuário não é staff, nem super user e for professor deve ser redirecionado para o home professor
@pytest.mark.django_db # permite acessar o banco de dados
def test_home_view_authenticated_staff_only_professor(client, user):
    user.is_staff = False
    user.is_professor = True
    user.is_superuser = False
    user.save()

    client.force_login(user)

    response = client.get(reverse('home'))
    assert response.status_code == 302
    assert response.url == reverse('home_professor')

# caso o usuário não tenha nenhuma permissão
@pytest.mark.django_db
def test_home_view_authenticated_staff_common_user(client, user):
    user.is_staff = False
    user.is_professor = False
    user.is_superuser = False
    user.save()

    client.force_login(user)

    response = client.get(reverse('home'))
    assert response.status_code == 200
    assert 'user/home.html' in [template.name for template in response.templates]

def test_signup_view(client):
    response = client.get(reverse('signup'))
    assert response.status_code == 200
    assert 'registration/signup.html' in [template.name for template in response.templates]

def test_logout_view(client):
    response = client.get(reverse('logout'))
    assert response.status_code == 302
    response = client.get(reverse('logout'), HTTP_ACCEPT_LANGUAGE='pt-br') # alguma coisa da tradução está bugando

# Teste para as páginas de erro
def test_404_handler(client):
    response = client.get('/nonexistent-url/')
    assert response.status_code == 404
    assert 'error/404.html' in [template.name for template in response.templates]

# Precisa testar de outra forma
@pytest.mark.django_db
def test_handler500(client):
    try:
        provocar_erro_500(None)
    except Exception:
        request = HttpRequest()
        request.path = '/qualquer_url/'
        request.user = None

        response = handler500(request)

    assert response.status_code == 500
