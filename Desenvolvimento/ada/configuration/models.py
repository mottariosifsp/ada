from django.db import models
from django.utils.translation import gettext_lazy as _

class Deadline(models.Model):
    name = models.CharField(_('name'), max_length=160)
    daedline_start = models.DateTimeField(_('deadline start'))
    deadline_end = models.DateTimeField(_('deadline end'))