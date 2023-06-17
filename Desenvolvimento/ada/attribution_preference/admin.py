from django.contrib import admin
from .models import Attribution_preference
from .models import Preference_schedule
from .models import Course_preference

class Attribution_preference_admin(admin.ModelAdmin):
    list_display = ('user',)

class Preference_schedule_admin(admin.ModelAdmin):
    list_display = ('attribution_preference', 'timeslot', 'day')

class Course_preference_admin(admin.ModelAdmin):
    list_display = ('attribution_preference', 'timetable',)
    search_fields = ('attribution_preference',)

admin.site.register(Attribution_preference, Attribution_preference_admin)
admin.site.register(Preference_schedule, Preference_schedule_admin)
admin.site.register(Course_preference, Course_preference_admin)