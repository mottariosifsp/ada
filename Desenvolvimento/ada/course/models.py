from django.db import models
from enums import enum
from django.utils.translation import gettext_lazy as _

class Course(models.Model):
    registration_course_id = models.CharField(_('registration course id'), max_length=45)
    name_course = models.CharField(_('course name'), max_length=45)
    period = models.CharField(_('period'), choices=[(s.name, s.value) for s in enum.Period], max_length=45)
    hour_start = models.TimeField(_('start time'))
    hour_end = models.TimeField(_('end time'))
    area = models.ForeignKey('area.Area', on_delete=models.CASCADE, related_name='courses')

    def __str__(self):
        return self.name_course
    