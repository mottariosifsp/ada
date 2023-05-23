from django.db import models

class Deadline(models.Model):
    name = models.CharField(_('name'), max_length=90)
    daedline_start = models.DateTimeField(_('deadline start'))
    deadline_end = models.DateTimeField(_('deadline end'))