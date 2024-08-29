from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', include('reports.urls')),
    path('', include(('reports.urls', 'reports'), namespace='reports')),
    path('main/', include('main.urls')),
    path('account/', include('account.urls')),
    path('material/', include('material.urls')),
    path('warehouse/', include('warehouse.urls')),
    path('orders/', include('orders.urls')),
    path('client/', include('client.urls')),
    #path('reports/', include('reports.urls', namespace='reports')),
 #   path('login/', LoginView.as_view(), name='login'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
