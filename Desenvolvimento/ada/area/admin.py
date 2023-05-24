from django.contrib import admin
from .models import Area

class Area_admin(admin.ModelAdmin):
    list_display = ('name_area', 'registration_area_id', 'exchange_area', 'is_high_school')
    search_fields = ('name_area', 'registration_area_id')

admin.site.register(Area, Area_admin)