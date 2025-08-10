from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    # order
    path('order/', views.OrderListView.as_view(), name='view_order'),
    path('order/<int:pk>/', views.OrderDetailView.as_view(), name='detail_order'),
    path('order/create/', views.OrderCreateView.as_view(), name='add_order'),
    path('order/<int:pk>/update/', views.OrderUpdateView.as_view(), name='change_order'),
    path('order/<int:pk>/delete/', views.OrderDeleteView.as_view(), name='delete_order'),
    # product
    path('', views.ProductListView.as_view(), name='view_product'),
    path('import/', views.ProductImportView.as_view(), name='import_product'),
    path('create/', views.ProductCreateView.as_view(), name='add_product'),
    path('<int:pk>/update/', views.ProductUpdateView.as_view(), name='change_product'),
    path('<int:pk>/delete/', views.ProductDeleteView.as_view(), name='delete_product'),
    # adjustment
    path('adjustment/', views.AdjustmentListView.as_view(), name='view_adjustment'),
    path('adjustment/create/', views.AdjustmentCreateView.as_view(), name='add_adjustment'),
    path('adjustment/<int:pk>/delete/', views.AdjustmentDeleteView.as_view(), name='delete_adjustment'),
]
