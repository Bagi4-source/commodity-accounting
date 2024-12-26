from django.contrib import admin
from .models import Product, ProductAttribute, Warehouse, Stock

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('sku', 'name', 'price')
    search_fields = ('sku', 'name')
    list_filter = ('price',)
    ordering = ('name',)
    fields = ('sku', 'name', 'price', 'description')

@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('product', 'attribute_name', 'attribute_value')
    search_fields = ('attribute_name', 'attribute_value', 'product__name')
    list_filter = ('attribute_name',)

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    search_fields = ('name', 'location')
    ordering = ('name',)

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('product', 'warehouse', 'quantity')
    search_fields = ('product__name', 'warehouse__name')
    list_filter = ('warehouse',)
    ordering = ('quantity',)