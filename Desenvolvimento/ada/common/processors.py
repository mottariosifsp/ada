def convert_to_uppercase(sender, instance, value):
    field_value = getattr(instance, sender.value)
    uppercase_value = field_value.upper()
    setattr(instance, sender.uppercase_field, uppercase_value)
