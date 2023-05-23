from django.urls import path
from user.views import home

urlpatterns = [
    path('', home, name='home'),
]