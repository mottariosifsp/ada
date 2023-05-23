from django.contrib import admin
from .models import Area, Block

class Area_admin(admin.ModelAdmin):
    list_display = ('name_area', 'registration_area_id', 'exchange_area', 'block_name')
    search_fields = ('name_area', 'registration_area_id')

    def block_name(self, obj):
        if obj.block:
            return obj.block.name_block
        else:
            return None

admin.site.register(Area, Area_admin)
admin.site.register(Block)