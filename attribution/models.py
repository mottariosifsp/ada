
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

from courses.models import Course

class TeacherCourseSelection(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('course',)

    def __str__(self):
        return f"{self.teacher} selected {self.course}"

class TeacherQueuePosition(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.IntegerField()

    def __str__(self):
        return f"{self.teacher} at position {self.position}"

    def clean(self):
        if self.position <= 0:
            raise ValidationError("Deve ser maior que 0")
