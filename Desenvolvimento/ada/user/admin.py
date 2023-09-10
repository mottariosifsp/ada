from django.contrib import admin
from .models import Proficiency, User, AcademicDegree, History
# Register your models here.

class User_admin(admin.ModelAdmin):
    # readonly_fields = ('password',)
    list_display = ('registration_id', 'first_name', 'email',)
    search_fields = ('registration_id', 'first_name', 'email',)

class AcademicDegree_admin(admin.ModelAdmin):
    list_display = ('name', 'punctuation',)
    search_fields = ('name', 'punctuation',)

admin.site.register(User, User_admin)
admin.site.register(AcademicDegree, AcademicDegree_admin)
admin.site.register(History)
admin.site.register(Proficiency)