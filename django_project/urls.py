from django.contrib import admin
from django.urls import path, include
from .views import home_view

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('product/', include('apps.product.urls')),
    path('material/', include('apps.material.urls')),
    path('process/', include('apps.process.urls')),
    path('core/', include('apps.core.urls')),
]
