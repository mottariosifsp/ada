from django.urls import path
from attribution.views import attribution, queueSetup

urlpatterns = [
    path('', attribution, name='attribution'),
    path('queueSetup', queueSetup, name='queueSetup')
]
