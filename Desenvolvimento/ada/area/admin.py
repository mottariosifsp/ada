from django.contrib import admin
from .models import Area, Block

class Area_admin(admin.ModelAdmin):
<<<<<<< HEAD
    list_display = ('name_area', 'registration_area_id', 'exchange_area', 'is_high_school')
=======
    list_display = ('name_area', 'registration_area_id', 'exchange_area', 'block_names')
>>>>>>> 0cd878babadd709af1672b2ec4748af38f141080
    search_fields = ('name_area', 'registration_area_id')

    def block_names(self, obj):
        return ", ".join([block.name_block for block in obj.blocks.all()])

    block_names.short_description = 'Block Names'

admin.site.register(Area, Area_admin)
admin.site.register(Block)