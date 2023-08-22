from django import forms
from django.core.exceptions import ValidationError

# validação campo
def validate_uppercase(value):
    if value != value.upper():
        raise ValidationError("Este campo deve conter apenas letras maiúsculas.")
    
# validação subir pro banco com maiúscula
def convert_to_uppercase(model, *fields):
    for field in fields:
        field_value = getattr(model, field)
        if field_value:
            setattr(model, field, str(field_value).upper())
    
# validação tamanho da sigla
def validate_acronym_length(value):
    if len(value) != 5:
        raise forms.ValidationError('O acrônimo deve ter exatamente 5 caracteres.')

# validações sobre mesmo horário
def validate_incongruity_time(value):
    if value.hour_start > value.hour_end:
        raise ValidationError("O horário de fim ocorre antes do início.")
    if value.hour_start == value.hour_end:
        raise ValidationError("O horário de início não pode ser o mesmo de fim.")

# validações comparação diferentes horários
def validate_interrupted_time(model, value):
    objects = model.objects.all()

    for obj in objects:
        if obj.hour_start < value.hour_start < obj.hour_end or obj.hour_start < value.hour_end < obj.hour_end:
            raise ValidationError("O horário se sobrepõe a outro horário existente.")
        if obj.hour_start == value.hour_start and obj.hour_end == value.hour_end:
            raise ValidationError("O horário é o mesmo a outro horário existente.")