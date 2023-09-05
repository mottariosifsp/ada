from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
from user.views import home, privacy_policy
from django.conf.urls import handler404, handler500

handler404 = 'user.views.handler404'
handler500 = 'user.views.handler500'

admin_patterns = [
    path('prazo/', include("admin_ada.urls")),
    path('', admin.site.urls),
]

urlpatterns = [
    path('admin/',include(admin_patterns)),
    path('staff/', include("staff.urls")),
    path('professor/', include("professor.urls")),
    path('user/', include('user.urls')),
    path('atribuicao/', include('attribution.urls', namespace='attribution')),
    path("", home, name="home"),
    path('<str:user>/politica-de-privacidade/', privacy_policy, name="privacy_policy"),
]

urlpatterns += i18n_patterns ( # quais sessões serão internacionalizadas
    path('admin/', include(admin_patterns)),
    path('staff/', include("staff.urls")),
    path('professor/', include("professor.urls")),
    path('user/', include('django.contrib.auth.urls')),
    path('atribuicao/', include("attribution.urls")),
    path("", home, name="home"),
)