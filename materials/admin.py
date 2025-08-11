from django.contrib import admin
from .models import MaterialCategory, UnitOfMeasure, ConstructionMaterial, MaterialTransaction

@admin.register(MaterialCategory)
class MaterialCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(UnitOfMeasure)
class UnitOfMeasureAdmin(admin.ModelAdmin):
    list_display = ['name', 'abbreviation']
    search_fields = ['name', 'abbreviation']

@admin.register(ConstructionMaterial)
class ConstructionMaterialAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'unit_of_measure', 'price_per_unit', 'current_quantity', 'minimum_stock_level']
    list_filter = ['category', 'unit_of_measure']
    search_fields = ['name', 'notes']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(MaterialTransaction)
class MaterialTransactionAdmin(admin.ModelAdmin):
    list_display = ['material', 'transaction_type', 'quantity', 'unit_price', 'amount']
    list_filter = ['transaction_type']
    search_fields = ['material__name', 'reference', 'notes']
    readonly_fields = ['amount']
