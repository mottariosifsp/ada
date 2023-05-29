from django.db import models
from django.utils.translation import gettext_lazy as _

class Deadline(models.Model):
    name = models.CharField(_('name'), max_length=90)
    deadline_start = models.DateTimeField(_('deadline start'))
    deadline_end = models.DateTimeField(_('deadline end'))
    block = models.ForeignKey('area.Block', on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = _('deadline')
        verbose_name_plural = _('deadlines')

