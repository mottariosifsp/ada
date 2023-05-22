from django.contrib import admin
from .models import Attribution_preference
from .models import Preference_schedule
from .models import Teaching_support_activity_attribution
from .models import Teaching_support_activity
from .models import Workload_supplementation
from .models import Attribution_preference_course_preference
from .models import Course_preference

class Attribution_preference_admin(admin.ModelAdmin):
    list_display = ('user',)

class Preference_schedule_admin(admin.ModelAdmin):
    list_display = ('attribution_preference', 'timeslot', 'day')

class Teaching_support_activity_attribution_admin(admin.ModelAdmin):
    list_display = ('attribution_preference',)

class Teaching_support_activity_admin(admin.ModelAdmin):
    list_display = ('name', 'duration')
    search_fields = ('name',)

class Workload_supplementation_admin(admin.ModelAdmin):
    list_display = ('name', 'duration')
    search_fields = ('name',)

class Attribution_preference_course_preference_admin(admin.ModelAdmin):
    list_display = ('attribution_preference', 'course_preference')

class Course_preference_admin(admin.ModelAdmin):
    list_display = ('course', 'count_course', 'priority', 'period')
    search_fields = ('priority', 'period')

admin.site.register(Attribution_preference, Attribution_preference_admin)
admin.site.register(Preference_schedule, Preference_schedule_admin)
admin.site.register(Teaching_support_activity_attribution, Teaching_support_activity_attribution_admin)
admin.site.register(Teaching_support_activity, Teaching_support_activity_admin)
admin.site.register(Workload_supplementation, Workload_supplementation_admin)
admin.site.register(Attribution_preference_course_preference, Attribution_preference_course_preference_admin)
admin.site.register(Course_preference, Course_preference_admin)