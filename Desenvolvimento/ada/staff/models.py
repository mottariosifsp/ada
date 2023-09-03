from django.db import models
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from common.validator.validator import convert_to_uppercase

class Deadline(models.Model):
    name = models.CharField(_('name'), max_length=90, null=False, blank=False)
    deadline_start = models.DateTimeField(_('deadline start'))
    deadline_end = models.DateTimeField(_('deadline end'))
    semester = models.IntegerField(_('semester'), min_length=1, max_length=1, null=False, blank=False)
    blockk = models.ForeignKey('area.Blockk', on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = _('deadline')
        verbose_name_plural = _('deadlines')

    def clean(self):
        super().clean()
        convert_to_uppercase(self, 'name')

class Criteria(models.Model):
    name_criteria = models.CharField(('name criteria'), max_length=90, null=False, blank=False)
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

class Alert(models.Model):
    name_alert = models.CharField(_('name alert'), max_length=90, null=False, blank=False)
    created_by = models.ForeignKey('user.User', on_delete=models.CASCADE, null=True)
    title = models.CharField(_('title'), max_length=45, null=True, blank=True)
    description = models.TextField(_('description'), null=False, blank=False, max_length=500)
    blockk = models.ForeignKey('area.Blockk', on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = _('alert')
        verbose_name_plural = _('alerts')

    def clean(self):
        super().clean()
        convert_to_uppercase(self, 'name')

@receiver(models.signals.post_save, sender=Criteria)
def on_change(sender, instance, **kwargs): 
    if instance.is_select:
        for criteria in Criteria.objects.all():
            if criteria != instance:
                criteria.is_select = False
                criteria.save()
