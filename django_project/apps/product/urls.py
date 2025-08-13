from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    # buyer
    path('buyer/', views.BuyerListView.as_view(), name='view_buyer'),
    path('buyer/<int:pk>/', views.BuyerDetailView.as_view(), name='detail_buyer'),
    path('buyer/create/', views.BuyerCreateView.as_view(), name='add_buyer'),
    path('buyer/update/<int:pk>/', views.BuyerUpdateView.as_view(), name='change_buyer'),
    path('buyer/delete/<int:pk>/', views.BuyerDeleteView.as_view(), name='delete_buyer'),
    # order
    path('order/', views.OrderListView.as_view(), name='view_order'),
    path('order/<int:pk>/', views.OrderDetailView.as_view(), name='detail_order'),
    path('order/print/<int:pk>/', views.OrderPrintView.as_view(), name='print_order'),
    path('order/create/', views.OrderCreateView.as_view(), name='add_order'),
    path('order/update/<int:pk>/', views.OrderUpdateView.as_view(), name='change_order'),
    path('order/delete/<int:pk>/', views.OrderDeleteView.as_view(), name='delete_order'),
    # product
    path('', views.ProductListView.as_view(), name='view_product'),
    path('import/', views.ProductImportView.as_view(), name='import_product'),
    path('create/', views.ProductCreateView.as_view(), name='add_product'),
    path('update/<int:pk>/', views.ProductUpdateView.as_view(), name='change_product'),
    path('delete/<int:pk>/', views.ProductDeleteView.as_view(), name='delete_product'),
    # adjustment
    path('adjustment/', views.AdjustmentListView.as_view(), name='view_adjustment'),
    path('adjustment/create/', views.AdjustmentCreateView.as_view(), name='add_adjustment'),
    path('adjustment/delete/<int:pk>/', views.AdjustmentDeleteView.as_view(), name='delete_adjustment'),
]
