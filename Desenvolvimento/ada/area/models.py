from django.db import models
from django.utils.translation import gettext_lazy as _

class Area(models.Model):
    name_area = models.CharField(_('name area'), max_length=45)
    registration_area_id = models.CharField(_('registration area id'), max_length=20)
    exchange_area = models.BooleanField(_('exchange area'), default=True)

    def __str__(self):
        return self.name_area