# Generated by Django 4.1.7 on 2023-05-31 01:34

import common.validator.validator
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('registration_block_id', models.CharField(max_length=20, unique=True, verbose_name='registration block id')),
                ('name_block', models.CharField(max_length=90, unique=True, verbose_name='name block')),
                ('acronym', models.CharField(max_length=3, validators=[common.validator.validator.validate_uppercase, common.validator.validator.validate_acronym_length], verbose_name='acronym')),
            ],
            options={
                'verbose_name': 'block',
                'verbose_name_plural': 'blocks',
            },
        ),
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_area', models.CharField(max_length=45, unique=True, verbose_name='name area')),
                ('acronym', models.CharField(max_length=3, validators=[common.validator.validator.validate_uppercase, common.validator.validator.validate_acronym_length], verbose_name='acronym')),
                ('registration_area_id', models.CharField(max_length=20, unique=True, verbose_name='registration area id')),
                ('exchange_area', models.BooleanField(default=True, verbose_name='exchange area')),
                ('is_high_school', models.BooleanField(default=True, verbose_name='is high school')),
                ('blocks', models.ManyToManyField(blank=True, related_name='areas', to='area.block')),
            ],
            options={
                'verbose_name': 'area',
                'verbose_name_plural': 'areas',
            },
        ),
    ]
