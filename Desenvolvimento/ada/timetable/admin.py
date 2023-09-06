from django.contrib import admin
from .models import Day_combo, Timetable, Timeslot, Timetable_user

class Timetable_admin(admin.ModelAdmin):
    list_display = ('course', 'classs', 'day_combos', )
    search_fields = ('day_combos',)

    def day_combos(self, obj):
        return ", ".join([Day_combo.day for Day_combo in obj.day_combo.all()])

class Timeslot_admin(admin.ModelAdmin):
    readonly_fields = ('position',)
    list_display = ('position', 'hour_start', 'hour_end')
    search_fields = ('position', 'hour_start', 'hour_end')

class Day_combo_admin(admin.ModelAdmin):
    list_display = ('day', 'timeslot',)
    search_fields = ('day',)

    def timeslot(self, obj):
        return ", ".join([str(Timeslot.position) for Timeslot in obj.timeslots.all()])

actions = ['action_remove_all_attribution']

@admin.action(description='Remove all attribution from user')
def action_remove_all_attribution(modeladmin, request, queryset):
    for obj in queryset:
        obj.update(user=None)

class Timetable_user_admin(admin.ModelAdmin):
    list_display = ('timetable', 'user')

admin.site.register(Day_combo, Day_combo_admin)
admin.site.register(Timetable, Timetable_admin)
admin.site.register(Timeslot, Timeslot_admin)
admin.site.register(Timetable_user, Timetable_user_admin)