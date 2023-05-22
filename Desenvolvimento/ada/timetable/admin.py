from django.contrib import admin
from .models import Timetable
from .models import Timeslot
from .models import Timetable_user

class Timetable_admin(admin.ModelAdmin):
    list_display = ('day', 'timeslot', 'course', '_class')
    search_fields = ('day')

class Timeslot_admin(admin.ModelAdmin):
    list_display = ('name', 'hour_start', 'hour_end')
    search_fields = ('name', 'hour_start', 'hour_end')

class Timetable_user_admin(admin.ModelAdmin):
    list_display = ('timetable', 'user')

admin.site.register(Timetable, Timetable_admin, Timeslot_admin, Timetable_user_admin)
