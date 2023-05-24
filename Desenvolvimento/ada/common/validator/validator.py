from django.core.exceptions import ValidationError
from datetime import time

def validate_uppercase(value):
    if value != value.upper():
        raise ValidationError("Este campo deve conter apenas letras maiúsculas.")

def validate_interrupted_time(model, field_start, field_end):
    objects = model.objects.all()

    for obj in objects:
        start_time = getattr(obj, field_start)
        end_time = getattr(obj, field_end)

        if start_time >= end_time or end_time <= start_time:
            raise ValidationError("O horário se sobrepõe a outro horário existente.")