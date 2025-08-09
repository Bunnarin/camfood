from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('money/', views.MoneyView.as_view(), name='view_money'),
    # transaction
    path('transaction/', views.TransactionListView.as_view(), name='view_transaction'),
    path('transaction/create/', views.TransactionCreateView.as_view(), name='add_transaction'),
    path('transaction/<int:pk>/delete/', views.TransactionDeleteView.as_view(), name='delete_transaction'),
]
