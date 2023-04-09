from django.urls import path
from attribution.views import index

urlpatterns = [
    path('', index, name='index'),
]
