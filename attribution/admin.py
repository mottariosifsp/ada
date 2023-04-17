from django.contrib import admin
from .models import TeacherCourseSelection, TeacherQueuePosition

class TeacherCourseSelectionAdmin(admin.ModelAdmin):
    #couseselectionadmin list_display
    list_display = ('id', 'course_id', 'teacher_id')
    list_filter = ('course_id', 'teacher_id')
    search_fields = ('id', 'course_id', 'teacher_id')

admin.site.register(TeacherCourseSelection, TeacherCourseSelectionAdmin)
