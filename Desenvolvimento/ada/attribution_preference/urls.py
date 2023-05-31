from django.urls import path
from attribution_preference.views import attributionPreference, confirmAttributionPreference

urlpatterns = [
    path('criar-fpa/', attributionPreference, name='attributionPreference'),
    path('ver-fpa/', confirmAttributionPreference, name='confirmAttributionPreference'),
]