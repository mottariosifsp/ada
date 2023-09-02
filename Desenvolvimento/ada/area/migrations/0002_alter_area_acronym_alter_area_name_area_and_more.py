# Generated by Django 4.1.7 on 2023-08-30 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('area', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='area',
            name='acronym',
            field=models.CharField(max_length=10, unique=True, verbose_name='acronym'),
        ),
        migrations.AlterField(
            model_name='area',
            name='name_area',
            field=models.CharField(max_length=120, unique=True, verbose_name='name area'),
        ),
        migrations.AlterField(
            model_name='blockk',
            name='acronym',
            field=models.CharField(max_length=10, unique=True, verbose_name='acronym'),
        ),
    ]
