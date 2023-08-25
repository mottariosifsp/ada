from django.db import models
from django.dispatch import receiver
from common.processors import sort_by_time
from enums import enum
from django.utils.translation import gettext_lazy as _
from common.validator.validator import validate_incongruity_time, validate_interrupted_time

class Timetable(models.Model):
    course = models.ForeignKey('course.Course', on_delete=models.CASCADE, related_name='timetable', null=True, blank=True)
    classs = models.ForeignKey('classs.Classs', on_delete=models.CASCADE, related_name='timetable')
    day_combo = models.ManyToManyField('Day_combo', related_name='day_combos')
    class Meta:
        verbose_name = _('timetable')
        verbose_name_plural = _('timetables')
        
    def __str__(self):
        return str(self.course)
    
class Timeslot(models.Model):
    position = models.IntegerField(_('position'), null=True, blank=True)
    hour_start = models.TimeField(_('hour start'), null=False)
    hour_end = models.TimeField(_('hour end'), null=False)
    # area = models.ForeignKey('area.Area', on_delete=models.CASCADE, related_name='timeslot', null=True, blank=True)

    class Meta:
        verbose_name = _('timeslot')
        verbose_name_plural = _('timeslots')

    def __str__(self):
        return str(self.hour_start)
        
    def clean(self):
        super().clean()
        validate_incongruity_time(self) # validação hora início maior que a hora fim, validação hora início igual hora fim
        validate_interrupted_time(Timeslot, self) # validação uma hora em cima da outra, validação mesma hora
    
@receiver(models.signals.post_save, sender=Timeslot)
def execute_after_save(sender, instance, created, *args, **kwargs):
    if created:
        sort_by_time(Timeslot) # ordenação de horários

class Day_combo(models.Model):
    day_combo_id = models.AutoField(primary_key=True)
    day = models.CharField(_('day'), choices=[(s.name, s.value) for s in enum.Day], max_length=45)
    timeslots = models.ManyToManyField('Timeslot', related_name='day_combos')

    class Meta:
        verbose_name = _('day_combo')
        verbose_name_plural = _('day_combos')

    def __str__(self):
        return self.day

class Timetable_user(models.Model):
    timetable = models.ForeignKey('Timetable', on_delete=models.CASCADE, related_name='timetable_user')
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='timetable_user', null=True, blank=True)

    class Meta:
        verbose_name = _('timetable_user')
        verbose_name_plural = _('timetable_users')

    def __str__(self):
        return str(self.timetable.course)