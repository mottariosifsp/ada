from django.db import models
from enums import enum


class Course(models.Model):
    id_course = models.AutoField(primary_key=True)
    registration_course_id = models.CharField(max_length=45)
    name_course = models.CharField(max_length=45)
    period = models.CharField(choices=[(s.name, s.value) for s in enum.Period], max_length=45)
    hour_start = models.TimeField()
    hour_end = models.TimeField()
