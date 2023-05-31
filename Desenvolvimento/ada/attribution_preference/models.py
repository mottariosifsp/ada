from django.db import models
from enums import enum 
from django.utils.translation import gettext_lazy as _

class Attribution_preference(models.Model): #fpa
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    # adicionar uma chave estrageira de regras para regime

    class Meta:
        verbose_name = _('attribution_preference')
        verbose_name_plural = _('attribution_preferences')

    def __str__(self):
        return self.user.registration_id

class Preference_schedule(models.Model): # preferencia de horário
    attribution_preference = models.ForeignKey('Attribution_preference', on_delete=models.CASCADE)
    timeslot = models.ForeignKey('timetable.Timeslot', on_delete=models.CASCADE)
    day = models.CharField(_('day'), choices=[(s.name, s.value) for s in enum.Day], max_length=45)

    class Meta:
        verbose_name = _('preference_schedule')
        verbose_name_plural = _('preference_schedules')

    def __str__(self):
        return self.day

class Attribution_preference_course_preference(models.Model): 
    attribution_preference = models.ForeignKey('Attribution_preference', on_delete=models.CASCADE)
    course_preference = models.ForeignKey('Course_preference', on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('attribution_preference_course_preference')
        verbose_name_plural = _('attribution_preference_course_preferences')

class Course_preference(models.Model): #disciplinas
    course = models.ForeignKey('course.Course', on_delete=models.CASCADE)
    count_course = models.IntegerField(_('count course'))
    priority = models.CharField(_('priority'), choices=[(s.name, s.value) for s in enum.Priority], max_length=45)
    period = models.CharField(_('period'), choices=[(s.name, s.value) for s in enum.Period], max_length=45)

    class Meta:
        verbose_name = _('course_preference')
        verbose_name_plural = _('course_preferences')

    def __str__(self):
        return self.course.name_course
