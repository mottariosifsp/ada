from django.urls import path
from attribution.views import attribution, queueSetup, selectCourse 	

urlpatterns = [
    path('', attribution, name='attribution'),
    path('queueSetup', queueSetup, name='queueSetup'),
    path('selectCourse', selectCourse, name='selectCourse'),
]
