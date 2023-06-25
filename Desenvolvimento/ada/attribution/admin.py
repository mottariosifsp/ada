from django.contrib import admin
from .models import TeacherQueuePosition, TeacherQueuePositionBackup

class TeacherQueuePosition_admin(admin.ModelAdmin):
    list_display = ('teacher', 'position', 'blockk')
    search_fields = ('teacher', 'position', 'blockk')

class TeacherQueuePositionBackup_admin(admin.ModelAdmin):
    list_display = ('teacher', 'position', 'blockk')
    search_fields = ('teacher', 'position', 'blockk')

admin.site.register(TeacherQueuePosition, TeacherQueuePosition_admin)
admin.site.register(TeacherQueuePositionBackup, TeacherQueuePositionBackup_admin)
