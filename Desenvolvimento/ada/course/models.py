from django.db import models
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from common.processors import convert_to_uppercase
from common.validator.validator import validate_uppercase, validate_acronym_length
    
class Course(models.Model):
    registration_course_id = models.CharField(_('registration course id'), max_length=20, unique=True)
    name_course = models.CharField(_('course name'), max_length=45)
    acronym = models.CharField(_('acronym'), max_length=3, null=True, validators=[validate_acronym_length])
    area = models.ForeignKey('area.Area', on_delete=models.CASCADE, null=True)
    block = models.ForeignKey('area.Block', on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = _('course')
        verbose_name_plural = _('courses')

    def __str__(self):
        return self.name_course
    
@receiver(pre_save, sender=Course)
def convert_fields_to_uppercase(sender, instance, **kwargs):
    convert_to_uppercase(instance, 'registration_course_id', 'name_course', 'acronym')