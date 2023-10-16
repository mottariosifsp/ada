from django.contrib import admin
from .models import Course
# gource
class Course_admin(admin.ModelAdmin):
    list_display = ('registration_course_id', 'name_course', 'acronym', 'area', 'blockk')
    search_fields = ('registration_course_id', 'name_course', 'acronym')

admin.site.register(Course, Course_admin)