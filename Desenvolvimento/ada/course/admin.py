from django.contrib import admin
from .models import Course

class Course_admin(admin.ModelAdmin):
    list_display = ('id_course','registration_course_id','name_course', 'acronym', 'area', 'block')
    search_fields = ('id_course','registration_course_id','name_course', 'acronym')

admin.site.register(Course, Course_admin)