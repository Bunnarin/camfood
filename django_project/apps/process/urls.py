from django.urls import path
from . import views

app_name = 'process'

urlpatterns = [
    # purchase
    path('manufacturinglog/', views.ManufacturingLogListView.as_view(), name='view_manufacturinglog'),
    path('manufacturinglog/create/', views.ManufacturingLogCreateView.as_view(), name='add_manufacturinglog'),
    path('manufacturinglog/<int:pk>/delete/', views.ManufacturingLogDeleteView.as_view(), name='delete_manufacturinglog'),
]
