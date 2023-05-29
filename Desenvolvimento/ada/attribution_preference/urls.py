from django.urls import path
from attribution_preference.views import attributionPreference, confirmAttributionPreference

urlpatterns = [
    path('', attributionPreference, name='attributionPreference'),
    path('confirmar/', confirmAttributionPreference, name='confirmAttributionPreference'),
]