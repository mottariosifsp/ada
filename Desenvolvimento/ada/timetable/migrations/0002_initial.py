# Generated by Django 4.1.7 on 2023-06-02 03:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('course', '0001_initial'),
        ('area', '0001_initial'),
        ('classs', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('timetable', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='timetable_user',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='timetable_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='timetable',
            name='classs',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='timetable', to='classs.classs'),
        ),
        migrations.AddField(
            model_name='timetable',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='timetable', to='course.course'),
        ),
        migrations.AddField(
            model_name='timetable',
            name='timeslot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='timetable', to='timetable.timeslot'),
        ),
        migrations.AddField(
            model_name='timeslot',
            name='area',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='timeslot', to='area.area'),
        ),
    ]