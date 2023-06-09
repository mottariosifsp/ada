# Generated by Django 4.1.7 on 2023-06-08 14:57

import common.validator.validator
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('area', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='area',
            name='acronym',
            field=models.CharField(max_length=3, validators=[common.validator.validator.validate_acronym_length], verbose_name='acronym'),
        ),
        migrations.AlterField(
            model_name='blockk',
            name='acronym',
            field=models.CharField(max_length=3, validators=[common.validator.validator.validate_acronym_length], verbose_name='acronym'),
        ),
    ]
