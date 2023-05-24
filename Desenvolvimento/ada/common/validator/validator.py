from django.core.exceptions import ValidationError
from datetime import time

def validate_uppercase(value):
    if value != value.upper():
        raise ValidationError("Este campo deve conter apenas letras maiúsculas.")

def validate_interrupted_time(model, hour_start, hour_end):
    objects = model.objects.all()
    print(hour_start, hour_end)

    # for obj in objects:
    #     start_time = getattr(obj, field_start)
    #     end_time = getattr(obj, field_end)

    #     if start_time >= end_time and end_time <= start_time:
    #         raise ValidationError("O horário se sobrepõe a outro horário existente.")

    order = sorted(objects, key=lambda obj: getattr(obj, hour_start))
    print(hour_start, hour_end)

    for i in range(1, len(order)):
        horario_anterior = order[i-1]
        horario_atual = order[i]
        print("olar")
        hora_fim_anterior = getattr(horario_anterior, hour_end)
        hora_comeco_atual = getattr(horario_atual, hour_start)

        if hora_fim_anterior > hora_comeco_atual:
            raise ValidationError("A hora de término do horário anterior não pode ser maior que a hora de início do horário atual.")