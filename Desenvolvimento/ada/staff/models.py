from django.db import models
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from common.validator.validator import convert_to_uppercase

class Deadline(models.Model):
    name = models.CharField(_('name'), max_length=90)
    deadline_start = models.DateTimeField(_('deadline start'))
    deadline_end = models.DateTimeField(_('deadline end'))
    blockk = models.ForeignKey('area.Blockk', on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = _('deadline')
        verbose_name_plural = _('deadlines')

    def clean(self):
        super().clean()
        convert_to_uppercase(self, 'name')

class Criteria(models.Model):
    name_criteria = models.CharField(('name criteria'), max_length=90)
    number_criteria = models.IntegerField('number criteria', unique=True, null=True, blank=False)
    is_select = models.BooleanField(('is selected'), default=False)

    # def clean(self):
    #     if self.is_select and Criteria.objects.filter(is_select=True).exists():
    #         raise ValidationError('Only one Criteria can be selected at a time.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        convert_to_uppercase(self, 'name_criteria')

@receiver(models.signals.post_save, sender=Criteria)
def on_change(sender, instance, **kwargs): 
    if instance.is_select:
        for criteria in Criteria.objects.all():
            if criteria != instance:
                criteria.is_select = False
                criteria.save()
