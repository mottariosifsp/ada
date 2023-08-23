import pytest
from django.core.exceptions import ValidationError
from common.processors import sort_by_time
from datetime import time
from unittest.mock import Mock

from common.validator.validator import (
    validate_uppercase,
    convert_to_uppercase,
    validate_acronym_length,
    validate_incongruity_time,
    validate_interrupted_time,
)

class MockModel:
    pass

# Teste para o método que verifica se um campo possui apenas letras maiúsculas
def test_validate_uppercase():
    # Deve lançar uma exceção se for minúsculo
    with pytest.raises(ValidationError):
        validate_uppercase("lowercase")

    # Nenhuma exceção deve ser lançada
    validate_uppercase("UPPERCASE")

# Teste para o método que converte para letras maiúsculas
def test_convert_to_uppercase(monkeypatch):
    model = MockModel()
    model.field1 = "lowercase"
    model.field2 = "mIxEdCAsE"
    model.field3 = "UPPERCASE"

    monkeypatch.setattr(model, 'field1', model.field1)
    monkeypatch.setattr(model, 'field2', model.field2)
    monkeypatch.setattr(model, 'field3', model.field3)

    convert_to_uppercase(model, 'field1', 'field2', 'field3')

    assert model.field1 == "LOWERCASE"
    assert model.field2 == "MIXEDCASE"
    assert model.field3 == "UPPERCASE"

# TODO  - Os outros métodos do validator serão testados no timetable com teste unitário (apagar depois)