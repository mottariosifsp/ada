from django.db import models
from django.utils.translation import gettext_lazy as _
from common.validator.validator import convert_to_uppercase, validate_acronym_length
    
class Course(models.Model):
    registration_course_id = models.CharField(_('registration course id'), max_length=20, unique=True)
    name_course = models.CharField(_('course name'), max_length=45, unique=True)
    acronym = models.CharField(_('acronym'), max_length=5, null=True, unique=True, validators=[validate_acronym_length])
    area = models.ForeignKey('area.Area', on_delete=models.CASCADE, null=True)
    blockk = models.ForeignKey('area.Blockk', on_delete=models.CASCADE, null=True) 

    class Meta:
        verbose_name = _('course')
        verbose_name_plural = _('courses')

    def update_course(self, registration_course_id, name_course, acronym):
        self.registration_course_id = registration_course_id
        self.name_course = name_course
        self.acronym = acronym
        self.save()

    def __str__(self):
        return self.name_course 
    
    def clean(self):
        super().clean()
        convert_to_uppercase(self, 'name_course', 'acronym')