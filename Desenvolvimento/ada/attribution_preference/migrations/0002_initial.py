# Generated by Django 4.1.7 on 2023-11-01 16:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('area', '0001_initial'),
        ('attribution_preference', '0001_initial'),
        ('timetable', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='preference_schedule',
            name='timeslot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetable.timeslot'),
        ),
        migrations.AddField(
            model_name='course_preference',
            name='attribution_preference',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attribution_preference.attribution_preference'),
        ),
        migrations.AddField(
            model_name='course_preference',
            name='blockk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='area.blockk'),
        ),
        migrations.AddField(
            model_name='course_preference',
            name='timetable',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetable.timetable'),
        ),
    ]
