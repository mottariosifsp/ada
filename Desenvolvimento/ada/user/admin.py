from django.contrib import admin
from .models import User, AcademicDegree, History
# Register your models here.

class User_admin(admin.ModelAdmin):
    # readonly_fields = ('password',)
    list_display = ('registration_id', 'first_name', 'email',)
    search_fields = ('registration_id', 'first_name', 'email',)

# class AcademicDegree(admin.ModelAdmin):
#     list_display = ('registration_id', 'name', 'punctuation',)
#     search_fields = ('registration_id', 'name', 'punctuation',)

admin.site.register(User, User_admin)
admin.site.register(AcademicDegree)
admin.site.register(History)