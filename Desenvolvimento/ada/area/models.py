from django.db import models
from django.utils.translation import gettext_lazy as _


class Area(models.Model):
    name_area = models.CharField(_('name area'), max_length=45)
    registration_area_id = models.CharField(_('registration area id'), max_length=20)
    exchange_area = models.BooleanField(_('exchange area'), default=True)
    blocks = models.ManyToManyField('Block', blank=True)

    class Meta:
        verbose_name = _('area')
        verbose_name_plural = _('areas')

    def __str__(self):
        return self.name_area


class Block(models.Model):
    registration_block_id = models.AutoField(primary_key=True)
    name_block = models.CharField(_('name block'), max_length=45)

    class Meta:
        verbose_name = _('block')
        verbose_name_plural = _('blocks')

    def __str__(self):
        return self.name_block
