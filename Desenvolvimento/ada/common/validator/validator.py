from django.core.exceptions import ValidationError

def validate_uppercase(value):
    if value != value.upper():
        raise ValidationError("Este campo deve conter apenas letras maiúsculas.")

def validate_start_greater_end(value):
    if value.hour_start > value.hour_end:
        raise ValidationError("O horário de fim ocorre antes do início.")

def validate_interrupted_time(model, value):
    objects = model.objects.all()

    for obj in objects:
        if obj.hour_start < value.hour_start < obj.hour_end or obj.hour_start < value.hour_end < obj.hour_end:
            raise ValidationError("O horário se sobrepõe a outro horário existente.")