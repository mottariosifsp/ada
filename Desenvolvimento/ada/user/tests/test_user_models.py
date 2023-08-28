import pytest
from user.models import User, History, AcademicDegree

# Testes para os models do app User

# Criação de dados fictícios
@pytest.fixture
def academic_degrees():
    degree_1 = AcademicDegree.objects.create(name='Degree 1', punctuation=1)
    degree_2 = AcademicDegree.objects.create(name='Degree 2', punctuation=2)
    return [degree_1, degree_2]

@pytest.fixture
def history(academic_degrees):
    history = History.objects.create(
        birth='1990-01-01',
        date_career='2020-01-01',
        date_campus='2021-01-01',
        date_professor='2022-01-01',
        date_area='2023-01-01',
        date_institute='2024-01-01',
    )
    history.academic_degrees.set(academic_degrees)
    return history

@pytest.fixture
def user(history):
    return User.objects.create(
        first_name='João',
        last_name='Pereira',
        history=history
    )

# Método para criação de um History diferente
def create_new_history():
    return History.objects.create(
        birth='1995-02-01',
        date_career='1996-03-01',
        date_campus='1997-04-01',
        date_professor='1998-05-01',
        date_area='1999-06-01',
        date_institute='2000-07-01'
    )

# Testa o update do History do User (com academic degree diferente do original)
@pytest.mark.django_db
def test_update_history(user, history, academic_degrees):
    new_history = create_new_history()

    update_academic_degrees = [
        {'name': 'Degree 1 update', 'punctuation': 11},
        {'name': 'Degree 2 update', 'punctuation': 22},
    ]

    history.update_history(
        birth=new_history.birth,
        date_career=new_history.date_career,
        date_campus=new_history.date_campus,
        date_professor=new_history.date_professor,
        date_area=new_history.date_area,
        date_institute=new_history.date_institute,
        academic_degrees=update_academic_degrees
    )

    verify_updated_history(history, new_history, update_academic_degrees)

# Determina os academic degrees do usuário inicialmente
# Atualiza o History do User sem passar um novo academic degree ( pois ele pode ser vazio)
@pytest.mark.django_db
def test_update_history_without_academic_degrees(user, history, academic_degrees):
    new_history = create_new_history()

    history.update_history(
        birth=new_history.birth,
        date_career=new_history.date_career,
        date_campus=new_history.date_campus,
        date_professor=new_history.date_professor,
        date_area=new_history.date_area,
        date_institute=new_history.date_institute,
    )

    updated_user = User.objects.get(pk=user.pk)

    assert str(updated_user.history.birth) == str(new_history.birth)
    assert str(updated_user.history.date_career) == str(new_history.date_career)
    assert str(updated_user.history.date_campus) == str(new_history.date_campus)
    assert str(updated_user.history.date_professor) == str(new_history.date_professor)
    assert str(updated_user.history.date_area) == str(new_history.date_area)
    assert str(updated_user.history.date_institute) == str(new_history.date_institute)

    # Verifica se o academic degree é igual ao determinado inicialmente (def academic_degrees)
    updated_degrees = list(updated_user.history.academic_degrees.all())
    assert updated_degrees == academic_degrees

def verify_updated_history(history, new_history, update_academic_degrees):
    updated_history = History.objects.get(pk=history.pk)
    assert str(updated_history.birth) == str(new_history.birth)
    assert str(updated_history.date_career) == str(new_history.date_career)
    assert str(updated_history.date_campus) == str(new_history.date_campus)
    assert str(updated_history.date_professor) == str(new_history.date_professor)
    assert str(updated_history.date_area) == str(new_history.date_area)
    assert str(updated_history.date_institute) == str(new_history.date_institute)

    updated_degrees = list(updated_history.academic_degrees.all())

    for updated_degree, expected_degree in zip(updated_degrees, update_academic_degrees):
        assert updated_degree.name == expected_degree['name']
        assert updated_degree.punctuation == expected_degree['punctuation']

# Teste para capturar a junção do primeiro nome e a primeira letra do último nome junto com o "."
@pytest.mark.django_db
def test_get_first_name_and_last_initial(user):
    result = user.get_first_name_and_last_initial()
    assert result == 'João P.'

