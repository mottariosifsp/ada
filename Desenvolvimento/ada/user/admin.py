from django.contrib import admin
from .models import User, History, AcademicDegree

# Register your models here.

admin.site.register(User)
admin.site.register(AcademicDegree)
admin.site.register(History)
