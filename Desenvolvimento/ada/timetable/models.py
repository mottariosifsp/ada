from django.db import models
from enums import enum
from django.utils.translation import gettext_lazy as _
from common.validator.validator import validate_incongruity_time, validate_interrupted_time

class Timetable(models.Model):
    day = models.CharField(_('day'), choices=[(s.name, s.value) for s in enum.Day], max_length=45)
    timeslot = models.ForeignKey('Timeslot', on_delete=models.CASCADE, related_name='timetable')
    course = models.ForeignKey('course.Course', on_delete=models.CASCADE, related_name='timetable')
    _class = models.ForeignKey('class.Class', on_delete=models.CASCADE, related_name='timetable')
    
class Timeslot(models.Model):
    hour_start = models.TimeField(_('hour start'))
    hour_end = models.TimeField(_('hour end'))
    name = models.CharField(_('name'), max_length=10)

    def clean(self):
        super().clean()
        validate_incongruity_time(self) # validação hora início maior que a hora fim, validação hora início igual hora fim
        validate_interrupted_time(Timeslot, self) # validação uma hora em cima da outra

    def __str__(self):
        return self.name
    
class Timetable_user(models.Model):
    timetable = models.ForeignKey('Timetable', on_delete=models.CASCADE, related_name='timetable_user')
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='timetable_user')