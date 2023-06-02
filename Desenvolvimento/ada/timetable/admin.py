from django.contrib import admin
from .models import Timetable
from .models import Timeslot
from .models import Timetable_user

class Timetable_admin(admin.ModelAdmin):
    list_display = ('day', 'timeslot', 'course', 'classs')
    search_fields = ('day',)

class Timeslot_admin(admin.ModelAdmin):
    readonly_fields = ('position',)
    list_display = ('position', 'hour_start', 'hour_end', 'area')
    search_fields = ('position', 'hour_start', 'hour_end')

class Timetable_user_admin(admin.ModelAdmin):
    list_display = ('timetable', 'user')

admin.site.register(Timetable, Timetable_admin)
admin.site.register(Timeslot, Timeslot_admin)
admin.site.register(Timetable_user, Timetable_user_admin)