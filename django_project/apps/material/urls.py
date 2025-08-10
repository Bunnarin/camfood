from django.urls import path
from . import views

app_name = 'material'

urlpatterns = [
    # purchase
    path('purchase/', views.PurchaseListView.as_view(), name='view_purchase'),
    path('purchase/<int:pk>/', views.PurchaseDetailView.as_view(), name='detail_purchase'),
    path('purchase/create/', views.PurchaseCreateView.as_view(), name='add_purchase'),
    path('purchase/update/<int:pk>/', views.PurchaseUpdateView.as_view(), name='change_purchase'),
    path('purchase/delete/<int:pk>', views.PurchaseDeleteView.as_view(), name='delete_purchase'),
    # material
    path('', views.MaterialListView.as_view(), name='view_material'),
    path('import/', views.MaterialImportView.as_view(), name='import_material'),
    path('create/', views.MaterialCreateView.as_view(), name='add_material'),
    path('update/<int:pk>/', views.MaterialUpdateView.as_view(), name='change_material'),
    path('delete/<int:pk>/', views.MaterialDeleteView.as_view(), name='delete_material'),
    # adjustment
    path('adjustment/', views.AdjustmentListView.as_view(), name='view_adjustment'),
    path('adjustment/create/', views.AdjustmentCreateView.as_view(), name='add_adjustment'),
    path('adjustment/delete/<int:pk>/', views.AdjustmentDeleteView.as_view(), name='delete_adjustment'),
    # supplier
    path('supplier/', views.SupplierListView.as_view(), name='view_supplier'),
    path('supplier/create/', views.SupplierCreateView.as_view(), name='add_supplier'),
    path('supplier/delete/<int:pk>/', views.SupplierDeleteView.as_view(), name='delete_supplier'),
    path('supplier/update/<int:pk>/', views.SupplierUpdateView.as_view(), name='change_supplier'),
]
