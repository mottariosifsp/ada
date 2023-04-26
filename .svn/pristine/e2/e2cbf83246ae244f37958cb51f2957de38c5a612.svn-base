from django.urls import path
from attribution.views import attribution, queueSetup, selectCourse 	

urlpatterns = [
    path('', attribution, name='attribution'),
    #path('<str:lingua>/queueSetup/', queueSetup, name='queueSetup'),
    path('queueSetup/', queueSetup, name='queueSetup'),
    path('selectCourse', selectCourse, name='selectCourse'),
]
