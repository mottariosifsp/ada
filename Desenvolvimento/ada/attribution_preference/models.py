from django.db import models
from area.models import Blockk
from enums import enum
from django.utils.translation import gettext_lazy as _


class Attribution_preference(models.Model):  # fpa
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    year = models.CharField(_('year'), max_length=45, null=False, blank=False)
<<<<<<< HEAD
    name_job = models.CharField(
        _('name job'), choices=[
            (s.name, s.value) for s in enum.Job], max_length=45)
=======
    # job = models.ForeignKey(
    #     'user.Job',
    #     on_delete=models.CASCADE,)

>>>>>>> f197f8f429b843c1556acf6d4394a3e6522a4f9f
    class Meta:
        verbose_name = _('attribution_preference')
        verbose_name_plural = _('attribution_preferences')

    def __str__(self):
        return self.user.registration_id


class Preference_schedule(models.Model):  # preferencia de horário
    attribution_preference = models.ForeignKey(
        'Attribution_preference', on_delete=models.CASCADE)
    timeslot = models.ForeignKey(
        'timetable.Timeslot',
        on_delete=models.CASCADE)
    day = models.CharField(
        _('day'), choices=[
            (s.name, s.value) for s in enum.Day], max_length=45)

    class Meta:
        verbose_name = _('preference_schedule')
        verbose_name_plural = _('preference_schedules')

    def __str__(self):
        return self.day


class Course_preference(models.Model):  # disciplinas
    attribution_preference = models.ForeignKey(
        'Attribution_preference', on_delete=models.CASCADE)
    timetable = models.ForeignKey(
        'timetable.Timetable',
        on_delete=models.CASCADE)
    blockk = models.ForeignKey(Blockk, on_delete=models.CASCADE)
    priority = models.CharField(
        _('priority'), choices=[
            (s.name, s.value) for s in enum.Priority], max_length=45)

    class Meta:
        verbose_name = _('course_preference')
        verbose_name_plural = _('course_preferences')

    def __str__(self):
        return 'course_preference - ' + str(self.id)
