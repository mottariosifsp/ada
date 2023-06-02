from django.db import models
from django.utils.translation import gettext_lazy as _
from enums import enum

class Classs(models.Model):
    registration_class_id = models.CharField(_('registration class id'), max_length=20, unique=True)
    period = models.CharField(_('period'), choices=[(s.name, s.value) for s in enum.Period], max_length=45)
    semester = models.IntegerField(_('semester'))
    area = models.ForeignKey('area.Area', on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = _('classs')
        verbose_name_plural = _('classes')
        
    def get_semester_high_school(self):
        year = 0
        if self.area.is_high_school:
            year = (self.semester + 1) // 2
        else:
            year = self.semester
        return year

    def __str__(self):
        return self.registration_class_id