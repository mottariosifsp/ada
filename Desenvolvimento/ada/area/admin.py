from django.contrib import admin
from .models import Area, Block

class Area_admin(admin.ModelAdmin):
    list_display = ('registration_area_id', 'name_area', 'acronym', 'exchange_area', 'block_names', 'is_high_school')
    search_fields = ('registration_area_id', 'name_area', 'acronym')

    def block_names(self, obj):
        return ", ".join([block.name_block for block in obj.blocks.all()])

    block_names.short_description = 'Block Names'

class Block_admin(admin.ModelAdmin):
    list_display = ('registration_block_id', 'name_block', 'acronym')
    search_fields = ('registration_block_id', 'name_block', 'acronym')

admin.site.register(Area, Area_admin)
admin.site.register(Block, Block_admin)