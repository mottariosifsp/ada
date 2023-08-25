from django.urls import path
from django.contrib.auth import views as auth_views
from .views import deadline_configuration, deadline_configuration_confirm

urlpatterns = [
    path('', deadline_configuration, name='deadline_configuration'),
    path('confirmacao/', deadline_configuration_confirm, name='deadline_configuration_confirm')
]