# Generated by Django 4.1.7 on 2023-05-28 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('area', '0007_alter_area_options_alter_block_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='area',
            name='name_area',
            field=models.CharField(max_length=45, unique=True, verbose_name='name area'),
        ),
        migrations.AlterField(
            model_name='area',
            name='registration_area_id',
            field=models.CharField(max_length=20, unique=True, verbose_name='registration area id'),
        ),
    ]
