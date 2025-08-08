from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    # order
    path('order/', views.OrderListView.as_view(), name='view_order'),
    path('order/create/', views.OrderCreateView.as_view(), name='add_order'),
    path('order/<int:pk>/update/', views.OrderUpdateView.as_view(), name='change_order'),
    path('order/<int:pk>/delete/', views.OrderDeleteView.as_view(), name='delete_order'),
    # product
    path('/', views.ProductListView.as_view(), name='view_product'),
    path('/create/', views.ProductCreateView.as_view(), name='add_product'),
    path('/<int:pk>/update/', views.ProductUpdateView.as_view(), name='change_product'),
    path('/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='delete_product'),
]
