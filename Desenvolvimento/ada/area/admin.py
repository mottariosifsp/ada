from django.contrib import admin
from .models import Area, Blockk
# gource
class Area_admin(admin.ModelAdmin):
    list_display = ('registration_area_id', 'name_area', 'acronym', 'exchange_area', 'block_names', 'is_high_school')
    search_fields = ('registration_area_id', 'name_area', 'acronym')
    
    def block_names(self, obj):
        return ", ".join([blockk.name_block for blockk in obj.blocks.all()])

    block_names.short_description = 'Block Names'

class area_inline(admin.TabularInline):
    model = Area.blocks.through
    extra = 1


class Blockk_admin(admin.ModelAdmin):
    list_display = ('registration_block_id', 'name_block', 'acronym')
    search_fields = ('registration_block_id', 'name_block', 'acronym')
    inlines = [area_inline]


admin.site.register(Area, Area_admin)
admin.site.register(Blockk, Blockk_admin)