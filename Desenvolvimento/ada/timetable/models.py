from django.db import models
from django.dispatch import receiver
from common.processors import sort_by_time
from enums import enum
from django.utils.translation import gettext_lazy as _
from common.validator.validator import validate_incongruity_time, validate_interrupted_time

class Timetable(models.Model):
    day = models.CharField(_('day'), choices=[(s.name, s.value) for s in enum.Day], max_length=45)
    timeslot = models.ForeignKey('Timeslot', on_delete=models.CASCADE, related_name='timetable')
    course = models.ForeignKey('course.Course', on_delete=models.CASCADE, related_name='timetable')
    _class = models.ForeignKey('_class.Class', on_delete=models.CASCADE, related_name='timetable')

    class Meta:
        verbose_name = _('timetable')
        verbose_name_plural = _('timetables')
        
    def __str__(self):
        return self.day
    
class Timeslot(models.Model):
    position = models.IntegerField(_('position'), null=True, blank=True)
    hour_start = models.TimeField(_('hour start'))
    hour_end = models.TimeField(_('hour end'))
    area = models.ForeignKey('area.Area', on_delete=models.CASCADE, related_name='timeslot', null=True, blank=True)

    class Meta:
        verbose_name = _('timeslot')
        verbose_name_plural = _('timeslots')
<<<<<<< HEAD

    def __str__(self):
        return str(self.hour_start)
=======
>>>>>>> develop
        
    def clean(self):
        super().clean()
        validate_incongruity_time(self) # validação hora início maior que a hora fim, validação hora início igual hora fim
        validate_interrupted_time(Timeslot, self) # validação uma hora em cima da outra, validação mesma hora
    
@receiver(models.signals.post_save, sender=Timeslot)
def execute_after_save(sender, instance, created, *args, **kwargs):
    if created:
        sort_by_time(Timeslot) # ordenação de horários
        
class Timetable_user(models.Model):
    timetable = models.ForeignKey('Timetable', on_delete=models.CASCADE, related_name='timetable_user')
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='timetable_user')

    class Meta:
        verbose_name = _('timetable_user')
        verbose_name_plural = _('timetable_users')

    def __str__(self):
        return str(self.timetable.hour_start)