from django.urls import path
from .views import (
    DashboardView,
    MaterialListView, MaterialDetailView,
    MaterialCreateView, MaterialUpdateView, MaterialDeleteView,
    TransactionListView, TransactionCreateView,
    get_material_price
)

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    
    # Material URLs
    path('materials/', MaterialListView.as_view(), name='material-list'),
    path('materials/<int:pk>/', MaterialDetailView.as_view(), name='material-detail'),
    path('materials/add/', MaterialCreateView.as_view(), name='material-create'),
    path('materials/<int:pk>/edit/', MaterialUpdateView.as_view(), name='material-update'),
    path('materials/<int:pk>/delete/', MaterialDeleteView.as_view(), name='material-delete'),
    
    # Transaction URLs
    path('transactions/', TransactionListView.as_view(), name='transaction-list'),
    path('transactions/add/', TransactionCreateView.as_view(), name='transaction-create'),
    
    # API URLs
    path('api/materials/<int:material_id>/price/', get_material_price, name='material-price-api'),
]