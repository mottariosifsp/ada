from django.urls import path
from exchange.views import exchange
# gource
app_name = 'exchange'

urlpatterns = [
    path('permuta/', exchange, name='exchange'),
]