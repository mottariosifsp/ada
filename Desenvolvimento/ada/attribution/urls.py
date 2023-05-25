from django.urls import path
from attribution.views import queueSetup

urlpatterns = [
    path('queueSetup/', queueSetup, name='queueSetup'),
]