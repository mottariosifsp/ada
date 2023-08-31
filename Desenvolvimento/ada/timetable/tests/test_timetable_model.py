import pytest
from datetime import time
from django.core.exceptions import ValidationError
from timetable.models import Timeslot
from common.validator.validator import validate_incongruity_time, validate_interrupted_time

# Utilizado para simular um objeto que vem do banco de dados (QuerySet)
class MockQuerySet(list): # Herda da classe list
    def all(self): # Retorna todos os objetos do "banco de dados"
        return self

    def order_by(self, field):
        return self

# Simula a classe Timeslot
class MockManager:
    def __get__(self, instance, owner):
        return MockQuerySet([
            Timeslot(hour_start=time(12, 0), hour_end=time(13, 0)),
            Timeslot(hour_start=time(10, 0), hour_end=time(11, 0)),
            Timeslot(hour_start=time(15, 0), hour_end=time(16, 0))
        ])

# Teste do model timetable integrado ao validator
# Horário de início é anterior ao horário final - Não deve lançar exceção
def test_validate_incongruity_time_valid():
    timeslot = Timeslot(hour_start=time(9, 0), hour_end=time(10, 0))

    validate_incongruity_time(timeslot)


# Horário de início é posterior ao horário final - Deve lançar exceção
def test_validate_incongruity_time_invalid_before():
    timeslot = Timeslot(hour_start=time(11, 0), hour_end=time(10, 0))

    with pytest.raises(ValidationError) as exc_info:
        validate_incongruity_time(timeslot)

    assert "O horário de fim ocorre antes do início." in str(exc_info.value)


# Horário de início é igual ao horário final - Deve lançar exceção
def test_validate_incongruity_time_invalid_same_time():
    timeslot = Timeslot(hour_start=time(9, 0), hour_end=time(9, 0))

    with pytest.raises(ValidationError) as exc_info:
        validate_incongruity_time(timeslot)

    assert "O horário de início não pode ser o mesmo de fim." in str(exc_info.value)


# Testes para verificar a sobreposição de horário

# Horários corretos - Não deve lançar exceção
def test_validate_interrupted_time_no_overlap(monkeypatch):
    # Substituição para o MockManager
    monkeypatch.setattr(Timeslot, 'objects', MockManager())

    value = Timeslot(hour_start=time(9, 0), hour_end=time(10, 0))

    validate_interrupted_time(Timeslot, value)


def test_validate_interrupted_time_overlap(monkeypatch):
    # Dados fictícios
    mock_objects = [
        Timeslot(hour_start=time(8, 30), hour_end=time(9, 30)),
        Timeslot(hour_start=time(9, 15), hour_end=time(10, 15))
    ]

    # Retorna todos os objetos
    def mock_all():
        return mock_objects

    monkeypatch.setattr(Timeslot.objects, 'all', mock_all)

    value = Timeslot(hour_start=time(9, 0), hour_end=time(10, 0))

    # Deve lançar exceção, pois o horário está sobrepondo um já existente
    with pytest.raises(ValidationError) as exc_info:
        validate_interrupted_time(Timeslot, value)

    assert "O horário se sobrepõe a outro horário existente." in str(exc_info.value)


def test_validate_interrupted_time_same_time(monkeypatch):
    mock_objects = [
        Timeslot(hour_start=time(9, 0), hour_end=time(10, 0)),
        Timeslot(hour_start=time(10, 0), hour_end=time(11, 0))
    ]

    def mock_all():
        return mock_objects

    monkeypatch.setattr(Timeslot.objects, 'all', mock_all)

    # Deve lançar exceção, pois o horário é igual ao que tem no banco fictícios
    value = Timeslot(hour_start=time(9, 0), hour_end=time(10, 0))

    with pytest.raises(ValidationError) as exc_info:
        validate_interrupted_time(Timeslot, value)

    assert "O horário é o mesmo a outro horário existente." in str(exc_info.value)

# Teste quando os horário estão corretos
def test_validate_interrupted_time_different_time_and_no_overlap(monkeypatch):
    mock_objects = [
        Timeslot(hour_start=time(9, 0), hour_end=time(10, 0)),
        Timeslot(hour_start=time(10, 0), hour_end=time(11, 0))
    ]

    def mock_all():
        return mock_objects

    monkeypatch.setattr(Timeslot.objects, 'all', mock_all)

    value = Timeslot(hour_start=time(12, 0), hour_end=time(1, 0))

    validate_interrupted_time(Timeslot, value)
