from django.contrib import admin
from .models import Classs
# gource
class Classs_admin(admin.ModelAdmin):
    list_display = ('registration_class_id', 'period', 'semester', 'area')
    search_fields = ('registration_class_id', 'period', 'semester')

admin.site.register(Classs, Classs_admin)
