from django.contrib import admin
from .models import Deadline, Criteria

class Deadline_admin(admin.ModelAdmin):
    list_display = ('name_deadline','deadline_start','deadline_end')
    search_fields = ('name_deadline',)

admin.site.register(Deadline, Deadline_admin)

class Criteria_admin(admin.ModelAdmin):
    list_display = ('name_criteria','number_criteria','is_select')
    search_fields = ('name_criteria',)

admin.site.register(Criteria, Criteria_admin)

# class Classes_admin(admin.ModelAdmin):
#     list_display = ('registration_class_id', 'period', 'semester', 'area')
#     search_fields = ('registration_class_id', 'period', 'semester')

# Class = apps.get_model('class', 'Class')
# admin.site.register(Class, Classes_admin)