from django.dispatch import receiver
from area.models import Blockk
from user.models import User
from django.db import models
from django.core.exceptions import ValidationError


class TeacherQueuePosition(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.IntegerField()
    blockk = models.ForeignKey(Blockk, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.teacher} at position {self.position}"

    def clean(self):
        if self.position <= 0:
            raise ValidationError("Deve ser maior que 0")


class TeacherQueuePositionBackup(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.IntegerField()
    blockk = models.ForeignKey(Blockk, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.teacher} at position {self.position}"

    def clean(self):
        if self.position <= 0:
            raise ValidationError("Deve ser maior que 0")


@receiver(models.signals.pre_save, sender=User)
def on_change(sender, instance, **kwargs):
    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return False
    if old_instance.is_professor and not instance.is_professor:
        TeacherQueuePosition.objects.filter(teacher=instance).delete()
