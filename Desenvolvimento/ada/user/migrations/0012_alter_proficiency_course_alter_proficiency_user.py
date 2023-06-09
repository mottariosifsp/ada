# Generated by Django 4.1.7 on 2023-05-23 02:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_auto_20230522_0358'),
        ('user', '0011_user_block'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proficiency',
            name='course',
            field=models.ForeignKey(max_length=255, null=True, on_delete=django.db.models.deletion.CASCADE, to='course.course'),
        ),
        migrations.AlterField(
            model_name='proficiency',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
