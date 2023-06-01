from django.contrib import admin
from .models import Class

class Class_admin(admin.ModelAdmin):
    list_display = ('registration_class_id', 'period', 'semester', 'area')
    search_fields = ('registration_class_id', 'period', 'semester')

admin.site.register(Class, Class_admin)
