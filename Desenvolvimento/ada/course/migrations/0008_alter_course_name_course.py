# Generated by Django 4.1.7 on 2023-05-30 18:57

import common.validator.validator
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0007_alter_course_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='name_course',
            field=models.CharField(max_length=45, unique=True, validators=[common.validator.validator.validate_uppercase], verbose_name='course name'),
        ),
    ]
