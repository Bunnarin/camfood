from django.urls import path
from . import views

app_name = 'process'

urlpatterns = [
    # formula
    path('formula/', views.FormulaListView.as_view(), name='view_formula'),
    path('formula/create/', views.FormulaCreateView.as_view(), name='add_formula'),
    path('formula/change/<int:pk>/', views.FormulaUpdateView.as_view(), name='change_formula'),
    path('formula/delete/<int:pk>', views.FormulaDeleteView.as_view(), name='delete_formula'),
    # log
    path('manufacturinglog/', views.ManufacturingLogListView.as_view(), name='view_manufacturinglog'),
    path('manufacturinglog/create/', views.ManufacturingLogCreateView.as_view(), name='add_manufacturinglog'),
    path('manufacturinglog/<int:pk>/delete/', views.ManufacturingLogDeleteView.as_view(), name='delete_manufacturinglog'),
]
