from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from enums import enum
import re
from area.models import Blockk, Area
from common.validator.validator import convert_to_uppercase

# Métodos de gerenciamento de usuário


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.history = None
        user.job = None
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    registration_id = models.CharField(
        _('registration id'),
        max_length=9,
        unique=True,
        null=False,
        blank=False)
    first_name = models.CharField(
        _('first name'),
        max_length=60,
        null=False,
        blank=False)
    last_name = models.CharField(
        _('last name'),
        max_length=200,
        null=False,
        blank=False)
    email = models.EmailField(
        _('email address'),
        max_length=256,
        unique=True,
        null=False,
        blank=False)
    telephone = models.CharField(
        _('telephone'),
        max_length=11,
        null=True,
        blank=True)
    cell_phone = models.CharField(
        _('cell phone'),
        max_length=14,
        unique=True,
        null=False,
        blank=False)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_superuser = models.BooleanField(_('superuser status'), default=False)
    is_staff = models.BooleanField(_('staff status'), default=True)
    is_active = models.BooleanField(_('active'), default=True)  # mudar depois
    is_fgfcc = models.BooleanField(_('fgfcc'), default=False)
    is_professor = models.BooleanField(_('professor'), default=False)
    history = models.ForeignKey(
        'user.History',
        on_delete=models.CASCADE,
        blank=True,
        unique=True,
        null=True)
    job = models.ForeignKey(
        'user.Job',
        on_delete=models.CASCADE,
        blank=True,
        null=True)
    blocks = models.ManyToManyField(
        'area.Blockk',
        blank=True,
        related_name='user_blocks')
    objects = UserManager()

    USERNAME_FIELD = 'registration_id'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_job(self):
        if self.job.name_job == 'TWENTY_HOURS':
            return "20 horas"
        elif self.job.name_job == 'FOURTY_HOURS':
            return "40 horas"
        elif self.job.name_job == 'SUBSTITUTE':
            return "Substituto"
        elif self.job.name_job == 'TEMPORARY':
            return "Temporário"
        else:
            return "RDE"

    def get_full_name_camel_case(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.title().strip()

    def get_short_name(self):
        return self.first_name

    def format_telephone(self):
        telephone = self.telephone
        return f"({telephone[:2]}) {telephone[2:7]}-{telephone[7:]}"

    def format_cell_phone(self):
        cell_phone = self.cell_phone
        return f"({cell_phone[:2]}) {cell_phone[2:6]}-{cell_phone[6:]}"

    def get_first_name_and_last_initial(self):
        last_name_parts = self.last_name.split()
        last_name_last_word = last_name_parts[-1] if last_name_parts else ''
        last_name_initial = last_name_last_word[0] if last_name_last_word else ''
        return f"{self.first_name} {last_name_initial}."

    def get_initial(self):
        first_name_parts = self.first_name.split()
        last_name_parts = self.last_name.split()
        first_initial = first_name_parts[0][0] if first_name_parts else ''        
        last_name_last_word = last_name_parts[-1] if last_name_parts else ''
        last_name_initial = last_name_last_word[0] if last_name_last_word else ''
        
        return f"{first_initial} {last_name_initial}"

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def clean(self):
        super().clean()
        convert_to_uppercase(
            self,
            'registration_id',
            'first_name',
            'last_name'),

    def __str__(self):
        return str(self.first_name)


class AcademicDegreeHistory(models.Model):
    history = models.ForeignKey('History', on_delete=models.CASCADE)
    academic_degree = models.ForeignKey(
        'AcademicDegree', on_delete=models.CASCADE)
        


class History(models.Model):
    id_history = models.AutoField(primary_key=True)
    birth = models.DateField(_('birth'), null=False, blank=False)
    date_career = models.DateField(_('date career'), null=False, blank=False)
    date_campus = models.DateField(_('date campus'), null=False, blank=False)
    date_professor = models.DateField(
        _('date professor'), null=False, blank=False)
    date_area = models.DateField(_('date area'), null=False, blank=False)
    date_institute = models.DateField(
        _('date institute'), null=False, blank=False)
    academic_degrees = models.ManyToManyField(
        'AcademicDegree', blank=True, through='AcademicDegreeHistory')
    # blocks = models.ManyToManyField('area.Blockk', blank=True, related_name='history_blocks')

    def __str__(self):
        return str(self.id_history)

    def format_date(self, date):
        if date:
            return date.strftime("%d/%m/%Y")
        return ""

    def format_birth(self):
        return self.format_date(self.birth)

    def update_history(self, birth, date_career, date_campus, date_professor, date_area, date_institute,
                       academic_degrees=None):
        self.birth = birth
        self.date_career = date_career
        self.date_campus = date_campus
        self.date_professor = date_professor
        self.date_area = date_area
        self.date_institute = date_institute

        if academic_degrees is not None:
            academic_degrees_objs = []
            for degree_data in academic_degrees:
                name = degree_data['name']
                punctuation = int(degree_data['punctuation'])
                academic_degree, _ = AcademicDegree.objects.get_or_create(
                    name=name, punctuation=punctuation)
                academic_degrees_objs.append(academic_degree)

            self.academic_degrees.clear()
            self.academic_degrees.add(*academic_degrees_objs)

        self.save()


class AcademicDegree(models.Model):
    id_academic_degree = models.AutoField(primary_key=True)
    name = models.CharField(
        _('name'),
        max_length=256,
        unique=True,
        null=False,
        blank=False)
    punctuation = models.IntegerField()

    def __str__(self):
        return str(self.name)

    @classmethod
    def clean_up_unused_degrees(cls):
        unused_academic_degrees = cls.objects.filter(history__isnull=True)
        unused_academic_degrees.delete()

    def clean(self):
        super().clean()
        convert_to_uppercase(self, 'name')


class Job(models.Model):
    id_job = models.AutoField(primary_key=True)
    name_job = models.CharField(
        _('name job'), choices=[
            (s.name, s.value) for s in enum.Job], max_length=45)

    def __str__(self):
        return self.name_job

    def clean(self):
        super().clean()
        convert_to_uppercase(self, 'name_job')


class Proficiency(models.Model):
    id_proficiency = models.AutoField(primary_key=True)
    is_competent = models.BooleanField(_('is competent'), default=True)
    course = models.ForeignKey(
        'course.Course',
        on_delete=models.CASCADE,
        null=True)
    user = models.ForeignKey('user', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name_proficiency
