from django.db import models

class Deadline(models.Model):
    name = models.CharField(('name'), max_length=90)
    daedline_start = models.DateTimeField(('deadline start'))
    deadline_end = models.DateTimeField(('deadline end'))

class Criteria(models.Model):
    name_criteria = models.CharField(('name criteria'), max_length=45)
    is_select = models.BooleanField(('is selected'), default=False)
