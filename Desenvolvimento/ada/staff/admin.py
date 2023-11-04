from django.contrib import admin
from .models import Deadline, Criteria, Alert, Application_logs
# gource
class Deadline_admin(admin.ModelAdmin):
    list_display = ('name','deadline_start','deadline_end')
    search_fields = ('name',)

admin.site.register(Deadline, Deadline_admin)

class Criteria_admin(admin.ModelAdmin):
    list_display = ('name_criteria','number_criteria','is_select')
    search_fields = ('name_criteria',)

admin.site.register(Criteria, Criteria_admin)

class Alert_admin(admin.ModelAdmin):
    list_display = ('name_alert','created_by','title','description')
    search_fields = ('name_alert',)

class Application_logs_admin(admin.ModelAdmin):
    list_display = ('log_time','log_description')
    search_fields = ('log_description',)

 

admin.site.register(Alert, Alert_admin)
admin.site.register(Application_logs, Application_logs_admin)
# class Classes_admin(admin.ModelAdmin):
#     list_display = ('registration_class_id', 'period', 'semester', 'area')
#     search_fields = ('registration_class_id', 'period', 'semester')

# Class = apps.get_model('class', 'Class')
# admin.site.register(Class, Classes_admin)