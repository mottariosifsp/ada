from django.db import models

class Area(models.Model):
    name_area = models.CharField(max_length=45)
    registration_area_id = models.CharField(max_length=30)
    exchange_area = models.BooleanField(default=True)
# Create your models here.
