from django.contrib import admin
from .models import Deadline, Criteria

class Deadline_admin(admin.ModelAdmin):
    list_display = ('name','deadline_start','deadline_end')
    search_fields = ('name',)

admin.site.register(Criteria)