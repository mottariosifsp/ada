from django.urls import path
from django.contrib.auth import views as auth_views
from .views import home, signup, logout_view

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('sair/', logout_view, name='logout_view'),
]