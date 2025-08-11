from django import forms
from .models import (
    MaterialCategory, 
    UnitOfMeasure, 
    ConstructionMaterial,
    MaterialTransaction
)


class MaterialCategoryForm(forms.ModelForm):
    class Meta:
        model = MaterialCategory
        fields = ['name', 'description']

class UnitOfMeasureForm(forms.ModelForm):
    class Meta:
        model = UnitOfMeasure
        fields = ['name', 'abbreviation']

class ConstructionMaterialForm(forms.ModelForm):
    class Meta:
        model = ConstructionMaterial
        fields = [
            'name', 
            'category', 
            'unit_of_measure', 
            'price_per_unit',
            'minimum_stock_level',
            'notes'
        ]

class MaterialTransactionForm(forms.ModelForm):
    class Meta:
        model = MaterialTransaction
        fields = [
            'material',
            'transaction_type',
            'quantity',
            'unit_price',
            'reference',
            'notes'
        ]
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['material'].queryset = ConstructionMaterial.objects.all()