from django.urls import path
from attribution.views import queueSetup, queue

app_name = 'attribution'

urlpatterns = [
    path('queueSetup/', queueSetup, name='queueSetup'),
    path('queue/', queue, name='queue'),
]