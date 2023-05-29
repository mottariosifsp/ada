from django.contrib import admin
from .models import Deadline, Criteria

class Deadline_admin(admin.ModelAdmin):
    list_display = ('name','deadline_start','deadline_end')
    search_fields = ('name',)

admin.site.register(Deadline, Deadline_admin)

class Criteria_admin(admin.ModelAdmin):
    list_display = ('name_criteria','number_criteria','is_select')
    search_fields = ('name_criteria',)

admin.site.register(Criteria, Criteria_admin)