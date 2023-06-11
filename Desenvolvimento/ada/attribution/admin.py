from django.contrib import admin
from .models import TeacherQueuePosition

class TeacherQueuePosition_admin(admin.ModelAdmin):
    list_display = ('teacher', 'position', 'blockk')
    search_fields = ('teacher', 'position', 'blockk')

admin.site.register(TeacherQueuePosition, TeacherQueuePosition_admin)
