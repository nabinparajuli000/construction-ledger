from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import TemplateView
from django.db import models
from django.db.models import Sum
from django.http import JsonResponse
from .models import (
    MaterialCategory,
    UnitOfMeasure,
    ConstructionMaterial,
    MaterialTransaction
)
from .forms import (
    MaterialCategoryForm,
    UnitOfMeasureForm,
    ConstructionMaterialForm,
    MaterialTransactionForm
)

# Dashboard View
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'materials/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all materials
        materials = ConstructionMaterial.objects.all()
        context['materials'] = materials
        
        # Calculate total inventory value
        context['total_value'] = materials.aggregate(
            total_value=Sum(models.F('price_per_unit') * models.F('current_quantity'))
        )['total_value'] or 0
        
        # Get low stock items
        context['low_stock'] = materials.filter(
            current_quantity__lte=models.F('minimum_stock_level')
        )
        
        # Get recent transactions
        context['transactions'] = MaterialTransaction.objects.select_related('material')[:10]
        
        return context
# Material Views
class MaterialListView(LoginRequiredMixin, ListView):
    model = ConstructionMaterial
    template_name = 'materials/material_list.html'
    context_object_name = 'materials'
    paginate_by = 20

class MaterialDetailView(LoginRequiredMixin, DetailView):
    model = ConstructionMaterial
    template_name = 'materials/material_detail.html'
    context_object_name = 'material'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['transactions'] = MaterialTransaction.objects.filter(
            material=self.object
        ).order_by('-id')[:20]
        return context

class MaterialCreateView(LoginRequiredMixin, CreateView):
    model = ConstructionMaterial
    form_class = ConstructionMaterialForm
    template_name = 'materials/material_form.html'
    success_url = reverse_lazy('material-list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Material created successfully!')
        return super().form_valid(form)

class MaterialUpdateView(LoginRequiredMixin, UpdateView):
    model = ConstructionMaterial
    form_class = ConstructionMaterialForm
    template_name = 'materials/material_form.html'
    success_url = reverse_lazy('material-list')

    def form_valid(self, form):
        messages.success(self.request, 'Material updated successfully!')
        return super().form_valid(form)

class MaterialDeleteView(LoginRequiredMixin, DeleteView):
    model = ConstructionMaterial
    template_name = 'materials/material_confirm_delete.html'
    success_url = reverse_lazy('material-list')

    def delete(self, request, *args, **kwargs):
        material = self.get_object()
        # Check if there are related transactions
        transaction_count = MaterialTransaction.objects.filter(material=material).count()
        if transaction_count > 0:
            messages.warning(request, f'Cannot delete material "{material.name}" because it has {transaction_count} related transaction(s). Please delete the transactions first.')
            return redirect('material-detail', pk=material.pk)
        
        messages.success(request, f'Material "{material.name}" deleted successfully!')
        return super().delete(request, *args, **kwargs)

# Transaction Views
class TransactionListView(LoginRequiredMixin, ListView):
    model = MaterialTransaction
    template_name = 'materials/transaction_list.html'
    context_object_name = 'transactions'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        # Add filtering logic here if needed
        return queryset.order_by('-id')

class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = MaterialTransaction
    form_class = MaterialTransactionForm
    template_name = 'materials/transaction_form.html'
    success_url = reverse_lazy('transaction-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        # Here you would also create the ledger entry
        # This is a simplified version - you'd need to integrate with Django Ledger properly
        messages.success(self.request, 'Transaction recorded successfully!')
        return super().form_valid(form)


# API Views
def get_material_price(request, material_id):
    """API endpoint to get material price for transaction form"""
    try:
        material = get_object_or_404(ConstructionMaterial, id=material_id)
        return JsonResponse({'price': float(material.price_per_unit)})
    except (ValueError, TypeError):
        return JsonResponse({'price': 0.0})