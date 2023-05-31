from django.db import models
# from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
# from common.processors import convert_to_uppercase
from common.validator.validator import validate_acronym_length
    
class Course(models.Model):
    registration_course_id = models.CharField(_('registration course id'), max_length=20, unique=True)
    name_course = models.CharField(_('course name'), max_length=45, unique=True)
    acronym = models.CharField(_('acronym'), max_length=3, null=True, unique=True, validators=[validate_acronym_length])
    area = models.ForeignKey('area.Area', on_delete=models.CASCADE, null=True)
    block = models.ForeignKey('area.Block', on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = _('course')
        verbose_name_plural = _('courses')

    def __str__(self):
        return self.name_course
    
    # def save(self, *args, **kwargs):
    #     print("babababananananbabaNANA")
    #     super().save(*args, **kwargs)
    #     if self.area:
    #         blocks = self.area.get_blocks()
    #         if blocks:
    #             self.block = blocks.first()
    #     else:
    #         self.block = None
    #     super().save(*args, **kwargs)
    
# @receiver(pre_save, sender=Course)
# def convert_fields_to_uppercase(sender, instance, **kwargs):
#     convert_to_uppercase(instance, 'registration_course_id', 'name_course', 'acronym')

# @receiver(pre_save, sender=Course)
# def course_pre_save(sender, instance, **kwargs):
#     if instance.area:
#         blocks = instance.area.get_blocks()
#         if blocks:
#             instance.block = blocks.first()
#     else:
#         instance.block = None