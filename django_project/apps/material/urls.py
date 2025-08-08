from django.urls import path
from . import views

app_name = 'material'

urlpatterns = [
    # purchase
    path('purchase/', views.PurchaseListView.as_view(), name='view_purchase'),
    path('purchase/create/', views.PurchaseCreateView.as_view(), name='add_purchase'),
    path('purchase/<int:pk>/update/', views.PurchaseUpdateView.as_view(), name='change_purchase'),
    path('purchase/<int:pk>/delete/', views.PurchaseDeleteView.as_view(), name='delete_purchase'),
    # material
    path('/', views.MaterialListView.as_view(), name='view_material'),
    path('/create/', views.MaterialCreateView.as_view(), name='add_material'),
    path('/<int:pk>/update/', views.MaterialUpdateView.as_view(), name='change_material'),
    path('/<int:pk>/delete/', views.MaterialDeleteView.as_view(), name='delete_material'),
]
