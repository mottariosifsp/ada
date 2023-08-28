import pytest
from django.core.exceptions import ValidationError
from classs.models import Classs
from common.validator.validator import convert_to_uppercase
from area.models import Area


# Teste que verifica se é ensino médio ou não e captura o semestre
@pytest.mark.django_db
def test_classs_semester_high_school():
    area_high_school = Area.objects.create(
        registration_area_id='area-123',
        name_area='Técnico',
        acronym='TE',
        is_high_school=True
    )

    area_university = Area.objects.create(
        registration_area_id='area-456',
        name_area='Superior',
        acronym='SU',
        is_high_school=False
    )

    class_instance_high_school = Classs.objects.create(
        registration_class_id='class-125',
        period='MORNING',
        semester=3,
        area=area_high_school
    )

    class_instance_university = Classs.objects.create(
        registration_class_id='class-789',
        period='AFTERNOON',
        semester=4,
        area=area_university
    )

    assert class_instance_high_school.get_semester_high_school() == 2
    assert class_instance_university.get_semester_high_school() == 4
