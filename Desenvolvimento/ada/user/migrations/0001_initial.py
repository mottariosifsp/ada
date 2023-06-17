# Generated by Django 4.1.7 on 2023-06-17 02:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import user.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('course', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('area', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('registration_id', models.CharField(max_length=9, unique=True, verbose_name='registration id')),
                ('first_name', models.CharField(max_length=60, verbose_name='first name')),
                ('last_name', models.CharField(max_length=160, verbose_name='last name')),
                ('email', models.EmailField(max_length=160, unique=True, verbose_name='email address')),
                ('telephone', models.CharField(blank=True, max_length=11, null=True, verbose_name='telephone')),
                ('cell_phone', models.CharField(max_length=14, unique=True, verbose_name='cell phone')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=True, verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('is_professor', models.BooleanField(default=False, verbose_name='professor')),
                ('blocks', models.ManyToManyField(blank=True, related_name='user_blocks', to='area.blockk')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', user.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AcademicDegree',
            fields=[
                ('id_academic_degree', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=90, unique=True, verbose_name='name')),
                ('punctuation', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id_job', models.AutoField(primary_key=True, serialize=False)),
                ('name_job', models.CharField(max_length=160, unique=True, verbose_name='name job')),
            ],
        ),
        migrations.CreateModel(
            name='Proficiency',
            fields=[
                ('id_proficiency', models.AutoField(primary_key=True, serialize=False)),
                ('is_competent', models.BooleanField(default=True, verbose_name='is competent')),
                ('course', models.ForeignKey(max_length=255, null=True, on_delete=django.db.models.deletion.CASCADE, to='course.course')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id_history', models.AutoField(primary_key=True, serialize=False)),
                ('birth', models.DateField(verbose_name='birth')),
                ('date_career', models.DateField(verbose_name='date career')),
                ('date_campus', models.DateField(verbose_name='date campus')),
                ('date_professor', models.DateField(verbose_name='date professor')),
                ('date_area', models.DateField(verbose_name='date area')),
                ('date_institute', models.DateField(verbose_name='date institute')),
                ('academic_degrees', models.ManyToManyField(blank=True, to='user.academicdegree')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='history',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.history', unique=True),
        ),
        migrations.AddField(
            model_name='user',
            name='job',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.job'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
