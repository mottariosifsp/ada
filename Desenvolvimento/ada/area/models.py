from django.db import models
from django.utils.translation import gettext_lazy as _


class Area(models.Model):
    name_area = models.CharField(_('name area'), max_length=45)
    registration_area_id = models.CharField(_('registration area id'), max_length=20)
    exchange_area = models.BooleanField(_('exchange area'), default=True)
<<<<<<< HEAD
    is_high_school = models.BooleanField(_('is high school'), default=True)
=======
    blocks = models.ManyToManyField('Block', blank=True)

    def __str__(self):
        return self.name_area


class Block(models.Model):
    registration_block_id = models.AutoField(primary_key=True)
    name_block = models.CharField(_('name block'), max_length=45)
>>>>>>> 0cd878babadd709af1672b2ec4748af38f141080

    def __str__(self):
        return self.name_block
