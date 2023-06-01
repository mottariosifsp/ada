from django.urls import path
from .views import attribution_preference, confirm_attribution_preference

urlpatterns = [
    path('criar-fpa/', attribution_preference, name='attribution_preference'),
    path('ver-fpa/', confirm_attribution_preference, name='confirm_attribution_preference'),
]