# Generated by Django 4.1.7 on 2023-06-02 03:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('area', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Classs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_class_id', models.CharField(max_length=20, unique=True, verbose_name='registration class id')),
                ('period', models.CharField(choices=[('morning', 'MORNING'), ('afternoon', 'AFTERNOON'), ('night', 'NIGHT')], max_length=45, verbose_name='period')),
                ('semester', models.IntegerField(verbose_name='semester')),
                ('area', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='area.area')),
            ],
            options={
                'verbose_name': 'classs',
                'verbose_name_plural': 'classes',
            },
        ),
    ]