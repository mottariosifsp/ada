from django.db import models
from django.utils.translation import gettext_lazy as _
from common.validator.validator import validate_uppercase, validate_acronym_length

class Area(models.Model):
<<<<<<< HEAD
    name_area = models.CharField(_('name area'), max_length=45, unique=True)
    acronym = models.CharField(_('acronym'), max_length=3, validators=[validate_uppercase, validate_acronym_length])
    registration_area_id = models.CharField(_('registration area id'), max_length=20, unique=True)
=======
    name_area = models.CharField(_('name area'), max_length=90)
    registration_area_id = models.CharField(_('registration area id'), max_length=20)
>>>>>>> style/superadmin-change
    exchange_area = models.BooleanField(_('exchange area'), default=True)
    is_high_school = models.BooleanField(_('is high school'), default=True)
    blocks = models.ManyToManyField('Block', blank=False)

    class Meta:
        verbose_name = _('area')
        verbose_name_plural = _('areas')
    blocks = models.ManyToManyField('Block', blank=True, related_name='areas')

    def __str__(self):
        return self.name_area

    def get_blocks(self):
        return self.blocks.all()


class Block(models.Model):
<<<<<<< HEAD
    id = models.AutoField(primary_key=True, unique=True)
    registration_block_id = models.CharField(_('registration block id'), max_length=20, unique=True)
    name_block = models.CharField(_('name block'), max_length=90, unique=True)
    acronym = models.CharField(_('acronym'), max_length=3, validators=[validate_uppercase, validate_acronym_length])

    class Meta:
        verbose_name = _('block')
        verbose_name_plural = _('blocks')
=======
    registration_block_id = models.AutoField(primary_key=True)
    name_block = models.CharField(_('name block'), max_length=90)
>>>>>>> style/superadmin-change

    def __str__(self):
        return self.name_block
