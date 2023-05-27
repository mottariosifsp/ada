from django.contrib import admin
from .models import Class

class Class_admin(admin.ModelAdmin):
    list_display = ('registration_class_id', 'period', 'semester', 'is_high_school', 'area')
    search_fields = ('registration_class_id', 'semester')

admin.site.register(Class, Class_admin)
# Register your models here
