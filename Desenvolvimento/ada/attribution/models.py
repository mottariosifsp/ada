from user.models import User
from django.db import models
from django.core.exceptions import ValidationError

class TeacherQueuePosition(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.IntegerField()

    def __str__(self):
        return f"{self.teacher} at position {self.position}"

    def clean(self):
        if self.position <= 0:
            raise ValidationError("Deve ser maior que 0")
