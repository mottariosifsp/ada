from django.db import models
from django.core.exceptions import ValidationError

class Deadline(models.Model):
    name = models.CharField(('name'), max_length=90)
    daedline_start = models.DateTimeField(('deadline start'))
    deadline_end = models.DateTimeField(('deadline end'))

class Criteria(models.Model):
    name_criteria = models.CharField(('name criteria'), max_length=45)
    number_criteria = models.IntegerField('number criteria', unique=True, null=True, blank=False)
    is_select = models.BooleanField(('is selected'), default=False)

    def clean(self):
        if self.is_select and Criteria.objects.filter(is_select=True).exists():
            raise ValidationError('Only one Criteria can be selected at a time.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)