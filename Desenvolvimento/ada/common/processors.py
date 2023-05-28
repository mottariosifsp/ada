def convert_to_uppercase(sender, instance, value):
    field_value = getattr(instance, sender.value)
    uppercase_value = field_value.upper()
    setattr(instance, sender.uppercase_field, uppercase_value)

def sortByTime(model):
    count = 1
    for object in model.objects.all().order_by('hour_start'):
        object.position = count
        count += 1 
        object.save()
    print(model.objects.order_by('hour_start')[0].position)
