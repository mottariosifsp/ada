from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

# Métodos de gerenciamento de usuário
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, registration_id, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, registration_id=registration_id, **extra_fields)
        user.history = None
        user.job = None
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, registration_id, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, registration_id, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), max_length=100, unique=True)
    registration_id = models.CharField(_('registration id'), max_length=9, unique=True)
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)
    telephone = models.CharField(_('telephone'), max_length=10, null=True, blank=True)
    cell_phone = models.CharField(_('cell phone'), max_length=14)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_superuser = models.BooleanField(_('superuser status'), default=False)
    is_active = models.BooleanField(_('active'), default=True) #mudar depois
    is_staff = models.BooleanField(_('staff status'), default=True)
    history = models.ForeignKey('History', on_delete=models.CASCADE, null=True, blank=True)
    job = models.ForeignKey('Job', on_delete=models.CASCADE, null=True, blank=True)
    blocks = models.ManyToManyField('area.Block', blank=True)
    objects = UserManager()

    USERNAME_FIELD = 'registration_id'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

class History(models.Model):
    id_history = models.AutoField(primary_key=True) 
    birth = models.DateField(_('birth'))
    date_career = models.DateField(_('date career'))
    date_campus = models.DateField(_('date campus'))
    date_professor = models.DateField(_('date professor'))
    date_area = models.DateField(_('date area'))
    date_institute = models.DateField(_('date institute'))

    def __str__(self):
        return str(self.id_history)

class Job(models.Model):
    id_job = models.AutoField(primary_key=True)
    name_job = models.CharField(_('name job'), max_length=255)

    def __str__(self):
        return self.name_job
    
class Proficiency(models.Model):
    id_proficiency = models.AutoField(primary_key=True)
    is_competent = models.BooleanField(_('is competent'), default=True)
    course = models.ForeignKey('course.Course', max_length=255, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey('user', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name_proficiency