from django.urls import path
from attribution.views import queue_based_on_criterion

urlpatterns = [
    path('', queue_based_on_criterion, name='queue_based_on_criterion'),
]